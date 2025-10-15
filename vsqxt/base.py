from .setting import *
import traceback

class myError(Exception):
    def __init__(self,msg):
        self.msg=msg
    def __str__(self):
        return self.msg
    
class vPrm():
    def __init__(self,params):
        [bre,bri,cle,gen,ope]=params
        self.bre=bre
        self.bri=bri
        self.cle=cle
        self.gen=gen
        self.ope=ope
    def return_param(self):
        return [self.bre,self.bri,self.cle,self.gen,self.ope]
    def write2xml(self):
        vPrmStr=('<bre>'+str(self.bri)+'</bre>'+CHANGELINE+
		'<bri>'+str(self.bre)+'</bri>'+CHANGELINE+
		'<cle>'+str(self.cle)+'</cle>'+CHANGELINE+
		'<gen>'+str(self.gen)+'</gen>'+CHANGELINE+
		'<ope>'+str(self.ope)+'</ope>'+CHANGELINE)
        return vPrmStr

class vVoice():
    def __init__(self,params):
        [bs,pc,ID,name,vprm]=params
        self.bs=bs
        self.pc=pc
        self.ID=ID
        self.name=name
        self.vPrm=vPrm(vprm)
    def return_param(self):
        return [self.bs,self.pc,self.ID,self.name,self.vPrm]
    def write2xml(self):
        vVoiceStr=('<bs>'+str(self.bs)+'</bs>'+CHANGELINE+
		'<pc>'+str(self.pc)+'</pc>'+CHANGELINE+
		'<id><![CDATA['+str(self.ID)+']]></id>'+CHANGELINE+
		'<name><![CDATA['+str(self.name)+']]></name>'+CHANGELINE+
		'<vPrm>'+CHANGELINE+self.vPrm.write2xml()+'</vPrm>'+CHANGELINE)
        return vVoiceStr





class wavPart():
    def __init__(self,params):
        [t,playTime,name,comment,fs,rs,nCh,filePath]=params
        self.t=t
        self.playTime=playTime
        self.name=name
        self.comment=comment
        self.fs=fs
        self.rs=rs
        self.nCh=nCh
        self.filePath=filePath
    def return_param(self):
        return [self.t,self.playTime,self.name,self.comment,self.fs,self.rs,self.nCh,self.filePath]
    def write2xml(self):
        wavpartSTR=('<t>'+str(self.t)+'</t>'+CHANGELINE+
                    '<playTime>'+str(self.playTime)+'</playTime>'+CHANGELINE+
                    '<name><![CDATA['+str(self.name)+']]></name>'+CHANGELINE+
                    '<comment><![CDATA['+str(self.comment)+']]></comment>'+CHANGELINE+
                    '<fs>'+str(self.fs)+'</fs>'+CHANGELINE+
                    '<rs>'+str(self.rs)+'</rs>'+CHANGELINE+
                    '<nCh>'+str(self.nCh)+'</nCh>'+CHANGELINE+
                    '<filePath><![CDATA['+str(self.filePath)+']]></filePath>'+CHANGELINE)
        return wavpartSTR
class monoTrack():
    def __init__(self,wavPartList):# 只有一个参数，只输入一个二维列表
        self.wavPart=[]
        for wav in wavPartList:
            self.wavPart.append(wavPart(wav))
    def return_param(self):
        return self.wavPart
    def __write_wavPart__(self):
        if len(self.wavPart)==0:
            return ''
        s=''
        for wav in self.wavPart:
            s+='<wavPart>'+CHANGELINE+wav.write2xml()+'</wavPart>'+CHANGELINE
        return s
    def write2xml(self):
        monoTrackSTR=self.__write_wavPart__()
        return monoTrackSTR

class stTrack():
    def __init__(self,wavPartList):# 只有一个参数，只输入一个二维列表
        self.wavPart=[]
        for wav in wavPartList:
            self.wavPart.append(wavPart(wav))
    def return_param(self):
        return self.wavPart
    def __write_wavPart__(self):
        if len(self.wavPart)==0:
            return ''
        s=''
        for wav in self.wavPart:
            s+='<wavPart>'+CHANGELINE+wav.write2xml()+'</wavPart>'+CHANGELINE
        return s
    def write2xml(self):
        stTrackSTR=self.__write_wavPart__()
        return stTrackSTR


class aux():
    def __init__(self,params):
        [ID,content]=params
        self.ID=ID
        self.content=content
    def return_param(self):
        return [self.ID,self.content]
    def write2xml(self):
        auxSTR=('<id><![CDATA['+str(self.ID)+']]></id>'+CHANGELINE+
                '<content><![CDATA['+str(self.content)+']]></content>'+CHANGELINE)
        return auxSTR



##vVoiceEG=[0,5,'BCNFCY43LB2LZCD4','MIKU_V4X_Original_EVEC',[0,0,0,0,0]]
##monoEG=[[11445,355,'NewPart','New WAV Part',44100,16,1,'MIKU_V4X_Original_br03.wav'],
##        [13770,314,'New WAV Part','New WAV Part',44100,16,1,r'C:\Users\hasee\Desktop\葱茵\素材\MIKU V4X Breath Sound\MIKU_V4X_Original\MIKU_V4X_Original_br04.wav']]
##        
##stTrackEG=[[7800,224730,'NewPart]','New WAV Part',44100,16,2,'untitled.wav'],[234360,224730,'NewPart]','New WAV Part',44100,16,2,r'C:\Users\hasee\Desktop\葱茵\素材\夜明け前に飛び乗って\untitled.wav']]
##
##auxEG=['AUX_VST_HOST_CHUNK_INFO',
##       'VlNDSwcAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA']
##v=vVoice(vVoiceEG)
##m=monoTrack(monoEG)
##st=stTrack(stTrackEG)
##au=aux(auxEG)
##s=''
##s+=v.write2xml()
##s+=m.write2xml()
##s+=st.write2xml()
##s+=au.write2xml()
##with open('test.txt','w') as f:
##    f.writelines(s)

class timeSig():
    def __init__(self,params):
        [m,nu,de]=params
        self.m=m
        self.nu=nu
        self.de=de
    def return_param(self):
        return [self.m,self.nu,self.de]
    def write2xml(self):
        timeSigStr=('<m>'+str(self.m)+
                    '</m><nu>'+str(self.nu)+'</nu><de>'
                    +str(self.de)+'</de>')
        return timeSigStr
    def returnBeat(self):
        return str(self.nu)+'/'+str(self.de)
        
class tempo():
    def __init__(self,params):
        [t,v]=params
        self.t=t
        self.v=v
    def return_param(self):
        return[self.t,self.v]
    def write2xml(self):
        tempoStr=('<t>'+str(self.t)+'</t><v>'+str(self.v)+'</v>')
        return tempoStr
    def returnBPM(self):
        return str(float(self.v)/100)

class masterTrack():
    def __init__(self,params):
        [seqName,comment,resolution,preMeasure,TimeSigs,Tempos]=params
        self.seqName=seqName
        self.comment=comment
        self.resolution=resolution
        self.preMeasure=preMeasure
        self.tempo=[]
        self.timeSig=[]
        for TimeSig in TimeSigs:
            self.timeSig.append(timeSig(TimeSig))
        for Tempo in Tempos:
            self.tempo.append(tempo(Tempo))
    def returnBPM(self):
        if len(self.tempo)==1:
            return self.tempo[0].returnBPM()
        else:
            return self.tempo
    def returnBeat(self):
        if len(self.timeSig)==1:
            return self.timeSig[0].returnBeat()
        else:
            return self.timeSig
    def return_param(self):
        return[self.seqName,self.comment,self.resolution,self.preMeasure,self.timeSig,self.tempo]
    def __write_timeSig__(self):
        if len(self.timeSig)==0:
            return ''
        s=''
        for ts in self.timeSig:
            s+=('<timeSig>'+ts.write2xml()+'</timeSig>'+CHANGELINE)
        return s
    def __write_tempo__(self):
        if len(self.tempo)==0:
            return ''
        s=''
        for ts in self.tempo:
            s+=('<tempo>'+ts.write2xml()+'</tempo>'+CHANGELINE)
        return s
    
    def write2xml(self):
        MasterTrackStr=('<seqName><![CDATA['+str(self.seqName)+']]></seqName>'+CHANGELINE+
                        '<comment><![CDATA['+str(self.comment)+']]></comment>'+CHANGELINE+
                        '<resolution>'+str(self.resolution)+'</resolution>'+CHANGELINE+
                        '<preMeasure>'+str(self.preMeasure)+'</preMeasure>'+CHANGELINE+
                        self.__write_timeSig__()+self.__write_tempo__())
        
        return MasterTrackStr

        
      
#eg
#masterTrackParam=['Untitled0','New VSQ File',480,4,[[0,4,4],[9,3,4],[16,4,4],[21,3,4]],[[0,29900],[7204,12000]]]

class plug():
    def __init__(self,param):
        [ID,name,sdkVer,nPrm,vPrm,presetNo,enable,bypass]=param
        self.ID=ID
        self.name=name
        self.sdkVer=sdkVer
        self.nPrm=nPrm
        self.vPrm=vPrm #字符串列表
        self.presetNo=presetNo
        self.enable=enable
        self.bypass=bypass
    def return_param(self):
        return[self.id,self.name,self.sdkVer,self.nPrm,self.vPrm,self.presetNo,self.enable,self.bypass]
    def __write_vPrm__(self):
        if len(self.vPrm)==0:
            return ''
        s='<vPrm>'+CHANGELINE
        for vprm in self.vPrm:
            s+='    <v>'
            s=s+str(vprm)
            s+='</v>'+CHANGELINE
        s+='</vPrm>'+CHANGELINE
        return s
    def write2xml(self):
        plugStr=('<id><![CDATA['+str(self.ID)+']]></id>'+CHANGELINE+
				'<name><![CDATA['+str(self.name)+']]></name>'+CHANGELINE+
				'<sdkVer>'+str(self.sdkVer)+'</sdkVer>'+CHANGELINE+
				'<nPrm>'+str(self.nPrm)+'</nPrm>'+CHANGELINE+
				self.__write_vPrm__()+
				'<presetNo>'+str(self.presetNo)+'</presetNo>'+CHANGELINE+
				'<enable>'+str(self.enable)+'</enable>'+CHANGELINE+
				'<bypass>'+str(self.bypass)+'</bypass>'+CHANGELINE)
        return plugStr

    
class vsUnit():
    def __init__(self,params):
        [tNo,iGin,plugs,sLvl,sEnable,m,s,pan,vol]=params
        ##plugs是2维列表！！
        if len(plugs)==0:
            self.plugs=[]
        else:
            self.plugs=[]
            for plug_param in plugs:
                self.plugs.append(plug(plug_param))
        self.tNo=tNo
        self.iGin=iGin
        self.sLvl=sLvl
        self.sEnable=sEnable
        self.m=m
        self.s=s
        self.pan=pan
        self.vol=vol
    def return_param(self):
        return[self.tNo,self.iGin,self.plugs,self.sLvl,self.sEnable,self.m,self.s,self.pan,self.vol]    
                
    def __write_plug__(self):
        if len(self.plugs)==0:
            return ''
        s=''
        for plg in self.plugs:
            s+='<plug>'+CHANGELINE+'    '
            s=s+plg.write2xml()
            s+='</plug>'+CHANGELINE
        return s

    def write2xml(self):
        vsUnitStr=('<tNo>'+str(self.tNo)+'</tNo>'+CHANGELINE+
                                '<iGin>'+str(self.iGin)+'</iGin>'+CHANGELINE+
                                 self.__write_plug__()+                 
                                '<sLvl>'+str(self.sLvl)+'</sLvl>'+CHANGELINE+
                                '<sEnable>'+str(self.sEnable)+'</sEnable>'+CHANGELINE+
                                '<m>'+str(self.m)+'</m>'+CHANGELINE+
                                '<s>'+str(self.s)+'</s>'+CHANGELINE+
                                '<pan>'+str(self.pan)+'</pan>'+CHANGELINE+
                                 '<vol>'+str(self.vol)+'</vol>'+CHANGELINE)
        return vsUnitStr


class monoUnit():
    def __init__(self,params):
        [iGin,plugs,sLvl,sEnable,m,s,pan,vol]=params
        ##plugs是2维列表！！
        if len(plugs)==0:
            self.plugs=[]
        else:
            self.plugs=[]
            for plug_param in plugs:
                self.plugs.append(plug(plug_param))
        self.iGin=iGin
        self.sLvl=sLvl
        self.sEnable=sEnable
        self.m=m
        self.s=s
        self.pan=pan
        self.vol=vol
    def return_param(self):
        return[self.iGin,self.plugs,self.sLvl,self.sEnable,self.m,self.s,self.pan,self.vol]    
                
    def __write_plug__(self):
        if len(self.plugs)==0:
            return ''
        s=''
        for plg in self.plugs:
            s+='<plug>'+CHANGELINE+'    '
            s=s+plg.write2xml()
            s+='</plug>'+CHANGELINE
        return s

    def write2xml(self):
        vsUnitStr=( '<iGin>'+str(self.iGin)+'</iGin>'+CHANGELINE+
                                 self.__write_plug__()+                 
                                '<sLvl>'+str(self.sLvl)+'</sLvl>'+CHANGELINE+
                                '<sEnable>'+str(self.sEnable)+'</sEnable>'+CHANGELINE+
                                '<m>'+str(self.m)+'</m>'+CHANGELINE+
                                '<s>'+str(self.s)+'</s>'+CHANGELINE+
                                '<pan>'+str(self.pan)+'</pan>'+CHANGELINE+
                                 '<vol>'+str(self.vol)+'</vol>'+CHANGELINE)
        return vsUnitStr




class stUnit():
    def __init__(self,params):
        [iGin,plugs,m,s,vol]=params
        ##plugs是2维列表！！
        if len(plugs)==0:
            self.plugs=[]
        else:
            self.plugs=[]
            for plug_param in plugs:
                self.plugs.append(plug(plug_param))
        self.iGin=iGin
        self.m=m
        self.s=s
        self.vol=vol
    def return_param(self):
        return[self.iGin,self.plugs,self.m,self.s,self.vol]    
                
    def __write_plug__(self):
        if len(self.plugs)==0:
            return ''
        s=''
        for plg in self.plugs:
            s+='<plug>'+CHANGELINE+'    '
            s=s+plg.write2xml()
            s+='</plug>'+CHANGELINE
        return s

    def write2xml(self):
        vsUnitStr=( '<iGin>'+str(self.iGin)+'</iGin>'+CHANGELINE+
                                 self.__write_plug__()+              
                                '<m>'+str(self.m)+'</m>'+CHANGELINE+
                                '<s>'+str(self.s)+'</s>'+CHANGELINE+
                                '<vol>'+str(self.vol)+'</vol>'+CHANGELINE)
        return vsUnitStr


class masterUnit():
    def __init__(self,params):
        [oDev,plugs,plugSR,rLvl,vol]=params
        ##plugs是2维列表！！
        #plugSR只有一个，所以是一维列表
        if len(plugs)==0:
            self.plugs=[]
        else:
            self.plugs=[]
            for plug_param in plugs:
                self.plugs.append(plug(plug_param))
        if len(plugSR)==0:
            self.plugSR=''
        else:
            self.plugSR=plug(plugSR)
        self.oDev=oDev
        self.rLvl=rLvl
        self.vol=vol
    def return_param(self):
        return [self.oDev,self.plugs,self.plugSR,self.rLvl,self.vol]    
                
    def __write_plug__(self):
        if len(self.plugs)==0:
            return ''
        s=''
        for plg in self.plugs:
            s+='<plug>'+CHANGELINE+'    '
            s=s+plg.write2xml()
            s+='</plug>'+CHANGELINE
        return s


    def __write_plugSR__(self):
        if self.plugSR=='':
            return ''
        s=''
        s+='<plugSR>'+CHANGELINE+'    '
        s=s+self.plugSR.write2xml()
        s+='</plugSR>'+CHANGELINE
        return s


    def write2xml(self):
        vsUnitStr=( '<oDev>'+str(self.oDev)+'</oDev>'+CHANGELINE+
                                 self.__write_plug__()+
                                self.__write_plugSR__()+
                                '<rLvl>'+str(self.rLvl)+'</rLvl>'+CHANGELINE+
                                '<vol>'+str(self.vol)+'</vol>'+CHANGELINE)
        return vsUnitStr

    
class mixer():
    #一个masterUnit，多个vsUnit，一个MomoUnit,一个stUnit
    def __init__(self,params):
        [masterUnit_param,vsUnits_param,MomoUnit_param,stUnit_param]=params
        self.masterUnit=masterUnit(masterUnit_param)
        self.monoUnit=monoUnit(MomoUnit_param)
        self.stUnit=stUnit(stUnit_param)
        self.vsUnits=[]
        if len(vsUnits_param)!=0:
            for vsUnit_param in vsUnits_param:
                vs=vsUnit(vsUnit_param)
                self.vsUnits.append(vs)

    def __write_vsUnit__(self):
        if len(self.vsUnits)==0:
            return ''
        s=''
        for vsunit in self.vsUnits:
            s+='<vsUnit>'+CHANGELINE+'    '
            s=s+vsunit.write2xml()
            s+='</vsUnit>'+CHANGELINE
        return s

    def write2xml(self):
        mixerStr=( '<masterUnit>'+CHANGELINE+self.masterUnit.write2xml()+'</masterUnit>'+CHANGELINE+
                                 self.__write_vsUnit__()+
                                '<monoUnit>'+CHANGELINE+self.monoUnit.write2xml()+'</monoUnit>'+CHANGELINE+
                                '<stUnit>'+CHANGELINE+self.stUnit.write2xml()+'</stUnit>'+CHANGELINE)
        return mixerStr

        
    

#eg
'''
mixparam=[[0,[['<![CDATA[vy26]]>','<![CDATA[V3Comp]]>',2,2,['10563103','5592517'],0,1,0]],['<![CDATA[H82m]]>','<![CDATA[H82 Harmonic Maximizer]]>',2,7,[0,0,0,0,'6869600',0,'16777216'],0,1,0],0,0],\
          
          [[0,0,[['<![CDATA[vy26]]>','<![CDATA[V3Comp]]>',2,2,['10563103','5592517'],0,1,0],['<![CDATA[vx21]]>','<![CDATA[V3Reverb]]>',2,3,['8388608','3355443','6710886'],0,1,0]],-898,1,0,0,64,0],\
           [1,0,[['<![CDATA[    ]]>','<![CDATA[]]>',0,0,[],0,0,0],['<![CDATA[sMax]]>', '<![CDATA[D82 Sonic Maximizer]]>',2,5,[0,0,0,0,'8388608'],0,1,0]],-227,1,0,0,64,0]],\
          
          [0,[['<![CDATA[L82m]]>','<![CDATA[L82 Loudness Maximizer]]>',2,5,[0,0,0,'1671068','16777216'],0,1,0]],-280,1,0,0,64,0],\
          [0,[['<![CDATA[    ]]>','<![CDATA[]]>',0,0,[],0,0,0],['<![CDATA[L82m]]>','<![CDATA[L82 Loudness Maximizer]]>',2,5,[0,0,0,'1671068','16777216'],0,1,0]],0,0,-129]]
'''

class seqcc():
    def __init__(self,param):
        [p,v]=param
        self.p=p
        self.v=v
    def return_param(self):
        return [self.p,self.v]
    def write2xml(self):
        seqccSTR='<p>'+str(self.p)+'</p><v>'+str(self.v)+'</v>'
        return seqccSTR
class Seq_vibDep():
    def __init__(self,seqccs_param):
        #seqcc_param=param
        if len(seqccs_param)==0:
            self.seqcc_param=[]
        else:
            self.seqcc_param=[]
            for seqcc_param in seqccs_param:
                self.seqcc_param.append(seqcc(seqcc_param))
    def return_param(self):
        return self.seqcc_param
    def __write_seqcc__(self):
        if len(self.seqcc_param)==0:
            return ''
        s=''
        for seq in self.seqcc_param:
            s+='<cc>'+seq.write2xml()+'</cc>'+CHANGELINE
        return s
    def write2xml(self):
        if len(self.seqcc_param)==0:
            return ''
        else:
            STR='<seq id="vibDep">'+CHANGELINE+self.__write_seqcc__()+'</seq>'+CHANGELINE
        return STR
        
class Seq_vibRate():
    def __init__(self,seqccs_param):
        #seqcc_param=param
        if len(seqccs_param)==0:
            self.seqcc_param=[]
        else:
            self.seqcc_param=[]
            for seqcc_param in seqccs_param:
                self.seqcc_param.append(seqcc(seqcc_param))
    def return_param(self):
        return self.seqcc_param
    def __write_seqcc__(self):
        if len(self.seqcc_param)==0:
            return ''
        s=''
        for seq in self.seqcc_param:
            s+='<cc>'+seq.write2xml()+'</cc>'+CHANGELINE
        return s
    def write2xml(self):
        if len(self.seqcc_param)==0:
            return ''
        else:
            STR='<seq id="vibRate">'+CHANGELINE+self.__write_seqcc__()+'</seq>'+CHANGELINE        
        return STR
    
class nStyle():
    def __init__(self,params):
        [accent,bendDep,bendLen,decay,fallPort,opening,risePort,vibLen,vibType,vibDep,vibRate]=params
        self.accent=accent
        self.bendDep=bendDep
        self.bendLen=bendLen
        self.decay=decay
        self.fallPort=fallPort
        self.opening=opening
        self.risePort=risePort
        self.vibLen=vibLen
        self.vibType=vibType
        self.vibDep=Seq_vibDep(vibDep)
        self.vibRate=Seq_vibRate(vibRate)
    def return_param(self):
        return [self.accent,self.bendDep,self.bendLen,self.decay,self.fallPort,self.opening,self.risePort,self.vibLen,self.vibType,self.vibDep,self.vibRate]
    def write2xml(self):
        nstyleStr=('<v id="accent">'+str(self.accent)+'</v>'+CHANGELINE+
					'<v id="bendDep">'+str(self.bendDep)+'</v>'+CHANGELINE+
					'<v id="bendLen">'+str(self.bendLen)+'</v>'+CHANGELINE+
					'<v id="decay">'+str(self.decay)+'</v>'+CHANGELINE+
					'<v id="fallPort">'+str(self.fallPort)+'</v>'+CHANGELINE+
					'<v id="opening">'+str(self.opening)+'</v>'+CHANGELINE+
					'<v id="risePort">'+str(self.risePort)+'</v>'+CHANGELINE+
					'<v id="vibLen">'+str(self.vibLen)+'</v>'+CHANGELINE+
					'<v id="vibType">'+str(self.vibType)+'</v>'+CHANGELINE+
					self.vibDep.write2xml()+self.vibRate.write2xml())
        return nstyleStr
class VNOTE():
    def __init__(self,params):
        [t,dur,n,v,y,p,nstyle,lock]=params
        self.t=t
        self.dur=dur
        self.n=n
        self.v=v
        self.y=y
        self.p=p
        self.nStyle=nStyle(nstyle)
        self.lock=lock

    def __write_lock__(self):
        if self.lock=='':
            return ''
        else:
            return ' lock="1"'

    def return_param(self):
        return [self.t,self.dur,self.n,self.v,self.y,self.p,self.nStyle]
    def write2xml(self):
        writeStr=('<t>'+str(self.t)+'</t>'+CHANGELINE+
		'<dur>'+str(self.dur)+'</dur>'+CHANGELINE+
		'<n>'+str(self.n)+'</n>'+CHANGELINE+
		'<v>'+str(self.v)+'</v>'+CHANGELINE+
		'<y><![CDATA['+str(self.y)+']]></y>'+CHANGELINE+
                '<p'+self.__write_lock__()+'><![CDATA['+str(self.p)+']]></p>'+CHANGELINE+
                '<nStyle>'+CHANGELINE+self.nStyle.write2xml()+'</nStyle>'+CHANGELINE)
        return writeStr

class VCC():
    def __init__(self,params):
        [t,ID,v]=params
        self.t=t
        self.ID=ID
        self.v=v
    def return_param(self):
        return [self.t,self.ID,self.v]
    def write2xml(self):
        ccSTR='<t>'+str(self.t)+'</t><v id="'+str(self.ID)+'">'+str(self.v)+'</v>'
        return ccSTR
    
##    for demand in root.getElementsByTagName('DEMAND'):
##    for tp in demand.getElementsByTagName('type'):
##        print(tp.getAttribute("id")


class sPlug():
    def __init__(self,params):
        [ID,name,version]=params
        self.ID=ID
        self.name=name
        self.version=version
    def return_param(self):
        return[self.ID,self.name,self.version]
    def write2xml(self):
        sPlugStr=('<id><![CDATA['+str(self.ID)+']]></id>'+CHANGELINE+
                  '<name><![CDATA['+str(self.name)+']]></name>'+CHANGELINE+
                  '<version><![CDATA['+str(self.version)+']]></version>'+CHANGELINE)
        return sPlugStr
        
class pStyle():
    def __init__(self,params):
        [accent,bendDep,bendLen,decay,fallPort,opening,risePort]=params
        self.accent=accent
        self.bendDep=bendDep
        self.bendLen=bendLen
        self.decay=decay
        self.fallPort=fallPort
        self.opening=opening
        self.risePort=risePort
    def return_param(self):
        return [self.accent,self.bendDep,self.bendLen,self.decay,self.fallPort,self.opening,self.risePort]
    def write2xml(self):
        sPlugStr=('<v id="accent">'+str(self.accent)+'</v>'+CHANGELINE+
                  '<v id="bendDep">'+str(self.bendDep)+'</v>'+CHANGELINE+
                  '<v id="bendLen">'+str(self.bendLen)+'</v>'+CHANGELINE+
                  '<v id="decay">'+str(self.decay)+'</v>'+CHANGELINE+
                  '<v id="fallPort">'+str(self.fallPort)+'</v>'+CHANGELINE+
                  '<v id="opening">'+str(self.opening)+'</v>'+CHANGELINE+
                  '<v id="risePort">'+str(self.risePort)+'</v>'+CHANGELINE)
        return sPlugStr    
class singer():
    def __init__(self,params):
        [t,bs,pc]=params
        self.t=t
        self.bs=bs
        self.pc=pc
    def return_param(self):
        return [self.t,self.bs,self.pc]
    def write2xml(self):
        singerSTR=('<t>'+str(self.t)+'</t>'+CHANGELINE+
		  '<bs>'+str(self.bs)+'</bs>'+CHANGELINE+
		  '<pc>'+str(self.pc)+'</pc>'+CHANGELINE)
        return singerSTR

class vsPart():
    def __init__(self,params):
        
        [t,playTime,name,comment,sPlugs,pStyles,singers,ccs,notes,plane]=params
        self.t=t
        self.playTime=playTime
        self.name=name
        self.comment=comment
        self.sPlug=sPlug(sPlugs)
        self.pStyle=pStyle(pStyles)
        self.singer=singer(singers)
        self.plane=plane
        self.VCC=[]
        for cc in ccs:
            self.VCC.append(VCC(cc))
        self.VNote=[]
        for note in notes:
            self.VNote.append(VNOTE(note))
        
    def return_param(self):
        return [self.t,self.playTime,self.name,self.comment,self.sPlug,self.pStyle,self.singer,self.ccs,self.notes,self.plane]
    def ChangeVCCID(self,ID):
        allID=['D','B','R','C','G','T','X','W','P','S',
               'd',b'','r','c','g','t','x','w','p','s',
               'DYN','BRN','BRI','CLE','GEN','POR','XSY','GWL','PIT','PBS',
               'dyn','brn','bri','cle','gen','por','xsy','gwl','pit','pbs']
        if ID not in allID:
            print(str(ID)+'is not acceptable')
            return False
        if ID in ['D','d','DYN','dyn']:
            return 'D'
        if ID in ['B','b','BRN','brn']:
            return 'B'
        if ID in ['R','r','BRI','bri']:
            return 'R'
        if ID in ['C','c','CLE','cle']:
            return 'C'
        if ID in ['G','g','GEN','gen']:
            return 'G'
        if ID in ['T','t','POR','por']:
            return 'T'
        if ID in ['X','x','XSY','xsy']:
            return 'X'
        if ID in ['W','w','GWL','gwl']:
            return 'W'
        if ID in ['P','p','PIT','pit']:
            return 'P'
        if ID in ['S','s','PBS','pbs']:
            return 'S'

    def getVCCbyID(self,search_type='DYN'):
        ID=self.ChangeVCCID(search_type)
        searchedVCC=[]
        for vcc in self.VCC:
            if vcc.ID==ID:
                searchedVCC.append(vcc)
        return searchVCC
    def InsertVNote(self,t='0',dur='1920',n='60',v='64',y='a',p='a',
                    accent='50',bendDep='8',bendLen='0',decay='50',
                    fallPort='0',opening='127',risePort='0',
                    vibLen='0',vibType='0',vibDep=[],vibRate=[],
                    lock=''):
        noteparams=[t,dur,n,v,y,p,[accent,bendDep,bendLen,decay,fallPort,opening,risePort,vibLen,vibType,vibDep,vibRate],lock]
        vnote=VNote(noteparams)
        self.VNote.append(vnote)
        #self,VNote=sorted(self.VNote)
    def InsertVCC(self, ID, value, t):
        vcc=VCC([t,ID,value])
        self.VCC.append(vcc)    
    def __write_VCC__(self):
        if len(self.VCC)==0:
            return ''
        s=''
        for cc in self.VCC:
            s+='<cc>'+cc.write2xml()+'</cc>'+CHANGELINE
        return s
    def __write_VNote__(self):
        if len(self.VNote)==0:
            return ''
        s=''
        for note in self.VNote:
            s+='<note>'+CHANGELINE+note.write2xml()+'</note>'+CHANGELINE
        return s
    def write2xml(self):
        vsPartStr=('<t>'+str(self.t)+'</t>'+CHANGELINE+
		    '<playTime>'+str(self.playTime)+'</playTime>'+CHANGELINE+
		    '<name><![CDATA['+str(self.name)+']]></name>'+CHANGELINE+
		    '<comment><![CDATA['+str(self.comment)+']]></comment>'+CHANGELINE+
		    '<sPlug>'+CHANGELINE+self.sPlug.write2xml()+'</sPlug>'+CHANGELINE+
                    '<pStyle>'+CHANGELINE+self.pStyle.write2xml()+'</pStyle>'+CHANGELINE+
                    '<singer>'+CHANGELINE+self.singer.write2xml()+'</singer>'+CHANGELINE+
                   self.__write_VCC__()+self.__write_VNote__()+
                   '<plane>'+str(self.plane)+'</plane>'+CHANGELINE)
        return vsPartStr    
    

       
class vsTrack():
    def __init__(self,params):
        [tNo,name,comment,vsParts]=params
        self.tNo=tNo
        self.name=name
        self.comment=comment
        self.vsPart=[]
        for vspart in vsParts:
            self.vsPart.append(vsPart(vspart))
    def return_param(self):
        return [self.tNo,self.name,self.comment,self.vsPart]
    def __write_vsPart__(self):
        if len(self.vsPart)==0:
            return ''
        s=''
        for part in self.vsPart:
            s+='<vsPart>'+CHANGELINE+part.write2xml()+'</vsPart>'+CHANGELINE
        return s
    def write2xml(self):
        vsTrackStr=('<tNo>'+str(self.tNo)+'</tNo>'+CHANGELINE+
		'<name><![CDATA['+str(self.name)+']]></name>'+CHANGELINE+
		'<comment><![CDATA['+str(self.comment)+']]></comment>'+CHANGELINE+
		self.__write_vsPart__())
        return vsTrackStr
    #---------------Test--------------------------------------------#  
    def return_all_note(self):
        all_note=[]
        for part in self.vsPart:
            all_note+=part.VNote
        return all_note
    def return_all_cc(self):
        all_cc=[]
        for part in self.vsPart:
            all_cc+=part.VCC
        return all_cc
    
    def getVCCbyID(self,search_type='DYN'):
        ID=self.vsPart[0].ChangeVCCID(search_type)
        searchedVCC=[]
        all_cc=self.return_all_cc()
        for vcc in all_cc:
            if vcc.ID==ID:
                searchedVCC.append(vcc)
        return searchedVCC
     
    def create_vspart(self,t='0',playTime='1920',name='NewPart',
                      comment='New Musical Part',sPlugs=[],
                      bStyles=[],singers=[],ccs=[],notes=[],plane=0):
        if sPlugs==[] or bStyles==[] or singers==[]:
            try:
                vsPartInfo=self.vsPart[0]
            except IndexError:
                raise myError("""cannot fingding the information of singers.
                                Try to create a part from Vocaloid or giving the params of sPlugs,bStyles and singers""")
            else:
                if sPlugs==[]:
                    sPlugs=vsPartInfo.sPlugs.return_param()
                if pStyles==[]:
                    pStyles=vsPartInfo.pStyles.return_param()
                if singers==[]:
                    singers=vsPartInfo.singer.return_param()
        vspart=[t,playTime,name,comment,sPlugs,pStyles,singers,ccs,notes,plane]
        self.vsPart.append(vsPart(vspart))
        #self.vsPart=sorted(self.vsPart)
    def create_note(self,t='0',dur='1920',n='60',v='64',y='a',p='a',
                    accent='50',bendDep='8',bendLen='0',decay='50',
                    fallPort='0',opening='127',risePort='0',
                    vibLen='0',vibType='0',vibDep=[],vibRate=[],
                    lock=''):
        for part in self.vsPart:
            if int(part.t)<=int(t) and int(part.t+part.playTime)>=int(t)+int(dur):
                part.InsertVNote(t,dur,n,v,y,p,
                                 accent,bendDep,bendLen,decay,fallPort,opening,
                                 risePort,vibLen,vibType,vibDep,vibRate,lock)
                return True
        raise myError('cannot find a fitting vspart.Try to using create_vspart to create a fitting vsPart')
        
    def create_cc(self, typ='D', value='64', t='0'):
        for part in self.vsPart:
            if int(part.t)<=int(t) and int(part.t+part.playTime)>=int(t):
                part.InsertVCC(typ,value,t)
                return True
        raise myError('cannot find a fitting vspart.Try to using create_vspart to create a fitting vsPart')
        
		
        
#eg
"""
vsTrackParam=[0,'Track','Track',
              [[7680,61440,'NewPart','New Musical Part',#vsPart
               ['ACA9C502-A04B-42b5-B2EB-5CEA36D16FCE','VOCALOID2 Compatible Style','3.0.0.1'],#sPlug
                [50,8,0,50,0,127,0], #pStyle
                [0,0,5],#singer
                [[210,'R',66],[330,'R',67],[390,'R',68]],#vcc
                [[60,2040,24,64,'a','a',#note1
                  [50,0,0,50,0,127,0,50,1,
                [[32768,64]],[[32768,50]]]
                  ],
                 [7680,1920,74,64,'a','a',
                  [50,0,0,50,0,127,0,0,0,[],[]]]#note2
                 ],0]]]#plane
"""                    
        
        

