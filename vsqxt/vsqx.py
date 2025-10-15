from .base import vVoice,monoTrack,stTrack,aux,vsTrack,mixer,masterTrack
from .setting import *
import xml
import xml.sax
import xml.dom.minidom

class VSQX4():
    
    def __init__(self,params):
        self.xmlInfo='<?xml version="1.0" encoding="UTF-8" standalone="no"?>'+CHANGELINE
        self.vsq4Info="""<vsq4 xmlns="http://www.yamaha.co.jp/vocaloid/schema/vsq4/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.yamaha.co.jp/vocaloid/schema/vsq4/ vsq4.xsd">"""+CHANGELINE
    
        [vender,version,vVoiceTables,mixers,masterTracks,vsTracks,monoTracks,stTracks,auxs]=params
        self.vender=vender
        self.version=version
        
        self.vVoiceTable=[]
        for singers in vVoiceTables:
            self.vVoiceTable.append(vVoice(singers))
        self.mixer=mixer(mixers)# Mixer实例，包括主轨、各副轨,Mono轨音量均衡等
        self.masterTrack=masterTrack(masterTracks)#主轨信息，包括曲速、节拍
        
        self.vsTrack=[]# vstrack信息，n个，列表形式返回
        for tracks in vsTracks:
            self.vsTrack.append(vsTrack(tracks))
        

        self.monoTrack=monoTrack(monoTracks)#monotrack文件信息，monotrack类
        self.stTrack=stTrack(stTracks)#伴奏文件
        self.aux=aux(auxs) #文件后缀
    def __write_vVoice__(self):
        if len(self.vVoiceTable)==0:
            return ''
        s=''
        for singer in self.vVoiceTable:
            s+='<vVoice>'+CHANGELINE+singer.write2xml()+'</vVoice>'+CHANGELINE
        return s
    def __write_vsTrack(self):
        if len(self.vsTrack)==0:
            return ''
        s=''
        for track in self.vsTrack:
            s+='<vsTrack>'+CHANGELINE+track.write2xml()+'</vsTrack>'+CHANGELINE
        return s
    def write2xml(self):
        s=('<vender><![CDATA['+str(self.vender)+']]></vender>'+CHANGELINE+
	'<version><![CDATA['+str(self.version)+']]></version>'+CHANGELINE+
           '<vVoiceTable>'+CHANGELINE+self.__write_vVoice__()+'</vVoiceTable>'+CHANGELINE+
           '<mixer>'+CHANGELINE+self.mixer.write2xml()+'</mixer>'+CHANGELINE+
           '<masterTrack>'+CHANGELINE+self.masterTrack.write2xml()+'</masterTrack>'+CHANGELINE+
           self.__write_vsTrack()+
           '<monoTrack>'+CHANGELINE+self.monoTrack.write2xml()+'</monoTrack>'+CHANGELINE+
           '<stTrack>'+CHANGELINE+self.stTrack.write2xml()+'</stTrack>'+CHANGELINE+
           '<aux>'+CHANGELINE+self.aux.write2xml()+'</aux>'+CHANGELINE)
        return s

    def write(self,filename,mode='w'):
        s=self.xmlInfo+self.vsq4Info+self.write2xml()+'</vsq4>'
        with open(filename,mode,encoding='utf-8') as f:
            f.writelines(s)

#eg

##masterTrackParam=['Untitled0','New VSQ File',480,4,[[0,4,4],[9,3,4],[16,4,4],[21,3,4]],[[0,29900],[7204,12000]]]
##mixparam=[[0,[['vy26','V3Comp>',2,2,['10563103','5592517'],0,1,0]],['<![CDATA[H82m]]>','<![CDATA[H82 Harmonic Maximizer]]>',2,7,[0,0,0,0,'6869600',0,'16777216'],0,1,0],0,0],\
##          
##          [[0,0,[['<![CDATA[vy26]]>','<![CDATA[V3Comp]]>',2,2,['10563103','5592517'],0,1,0],['<![CDATA[vx21]]>','<![CDATA[V3Reverb]]>',2,3,['8388608','3355443','6710886'],0,1,0]],-898,1,0,0,64,0],\
##           [1,0,[['<![CDATA[    ]]>','<![CDATA[]]>',0,0,[],0,0,0],['<![CDATA[sMax]]>', '<![CDATA[D82 Sonic Maximizer]]>',2,5,[0,0,0,0,'8388608'],0,1,0]],-227,1,0,0,64,0]],\
##          
##          [0,[['<![CDATA[L82m]]>','<![CDATA[L82 Loudness Maximizer]]>',2,5,[0,0,0,'1671068','16777216'],0,1,0]],-280,1,0,0,64,0],\
##          [0,[['<![CDATA[    ]]>','<![CDATA[]]>',0,0,[],0,0,0],['<![CDATA[L82m]]>','<![CDATA[L82 Loudness Maximizer]]>',2,5,[0,0,0,'1671068','16777216'],0,1,0]],0,0,-129]]
##vsTrackParam=[#track1
##                [0,'Track','Track',
##              [[7680,61440,'NewPart','New Musical Part',#vsPart
##               ['ACA9C502-A04B-42b5-B2EB-5CEA36D16FCE','VOCALOID2 Compatible Style','3.0.0.1'],#sPlug
##                [50,8,0,50,0,127,0], #pStyle
##                [0,0,5],#singer
##                [[210,'R',66],[330,'R',67],[390,'R',68]],#vcc
##                [[60,2040,24,64,'a','a',#note1
##                  [50,0,0,50,0,127,0,50,1,
##                [[32768,64]],[[32768,50]]]
##                  ],
##                 [7680,1920,74,64,'a','a',
##                  [50,0,0,50,0,127,0,0,0,[],[]]]#note2
##                 ],0]]]#plane
##              ]
##vVoiceEG=[[0,5,'BCNFCY43LB2LZCD4','MIKU_V4X_Original_EVEC',[0,0,0,0,0]]]
##monoEG=[[11445,355,'NewPart','New WAV Part',44100,16,1,'MIKU_V4X_Original_br03.wav'],
##        [13770,314,'New WAV Part','New WAV Part',44100,16,1,r'C:\Users\hasee\Desktop\葱茵\素材\MIKU V4X Breath Sound\MIKU_V4X_Original\MIKU_V4X_Original_br04.wav']]
##        
##stTrackEG=[[7800,224730,'NewPart]','New WAV Part',44100,16,2,'untitled.wav'],[234360,224730,'NewPart]','New WAV Part',44100,16,2,r'C:\Users\hasee\Desktop\葱茵\素材\夜明け前に飛び乗って\untitled.wav']]
##
##auxEG=['AUX_VST_HOST_CHUNK_INFO',
##       'VlNDSwcAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA']
##
##vsqx_params=['Yamaha corporation','4.0.0.3',vVoiceEG,mixparam,masterTrackParam,
##             vsTrackParam,monoEG,stTrackEG,auxEG]


def read(filename):    
    dom=xml.dom.minidom.parse(filename)
    root=dom.documentElement
    
    vsq4_params=[]#vender,version,vVoiceTables,mixers,masterTracks,vsTracks,monoTracks,stTracks,auxs
    vender=root.getElementsByTagName('vender')[0].firstChild.data
    version=root.getElementsByTagName('version')[0].firstChild.data
    vsq4_params.append(vender)
    vsq4_params.append(version)
    vVoiceTable=[]
    voicetable=root.getElementsByTagName('vVoiceTable')[0].getElementsByTagName('vVoice')
    if len(voicetable)!=0:
        for voice in voicetable:
            bs = voice.getElementsByTagName('bs')[0].firstChild.data
            pc = voice.getElementsByTagName('pc')[0].firstChild.data
            ID = voice.getElementsByTagName('id')[0].firstChild.data
            name = voice.getElementsByTagName('name')[0].firstChild.data

            bre=voice.getElementsByTagName('bre')[0].firstChild.data
            bri=voice.getElementsByTagName('bri')[0].firstChild.data
            cle=voice.getElementsByTagName('cle')[0].firstChild.data
            gen=voice.getElementsByTagName('gen')[0].firstChild.data
            ope=voice.getElementsByTagName('ope')[0].firstChild.data

            vPrm=[bre,bri,cle,gen,ope]
            
            vVoice=[bs,pc,ID,name,vPrm]
            vVoiceTable.append(vVoice)
            
    vsq4_params.append(vVoiceTable)
    
    ####################  MIXER ############################        
    mixer_get=root.getElementsByTagName('mixer')[0]
    mixer=[]
    #---------------------masterUnit----------------------------------------#
    master=mixer_get.getElementsByTagName('masterUnit')[0]
    masterUnit=[]
    masterUnit.append(master.getElementsByTagName('oDev')[0].firstChild.data)
    #plug
    plug_get=master.getElementsByTagName('plug')
    plugs=[]
    if len(plug_get)!=0:
        for plug in plug_get:
            ID=plug.getElementsByTagName('id')[0].firstChild.data
            try:
                name=plug.getElementsByTagName('name')[0].firstChild.data
            except AttributeError:
                name=''
            sdkVer=plug.getElementsByTagName('sdkVer')[0].firstChild.data
            nPrm=plug.getElementsByTagName('sdkVer')[0].firstChild.data
            vPrm=[]
            vs=plug.getElementsByTagName('vPrm')
            if len(vs)!=0:
                vs=vs[0].getElementsByTagName('v')
                for v in vs:
                    vPrm.append(v.firstChild.data)
                
            presetNo=plug.getElementsByTagName('presetNo')[0].firstChild.data
            enable=plug.getElementsByTagName('enable')[0].firstChild.data
            bypass=plug.getElementsByTagName('bypass')[0].firstChild.data
            plug_list=[ID,name,sdkVer,nPrm,vPrm,presetNo,enable,bypass]
            plugs.append(plug_list)


    plugSR_get=master.getElementsByTagName('plugSR')
    if len(plugSR_get)!=0:
        plugSR_get=plugSR_get[0]
        ID=plugSR_get.getElementsByTagName('id')[0].firstChild.data
        try:
            name=plugSR_get.getElementsByTagName('name')[0].firstChild.data
        except AttributeError:
            name=''
        sdkVer=plugSR_get.getElementsByTagName('sdkVer')[0].firstChild.data
        nPrm=plugSR_get.getElementsByTagName('nPrm')[0].firstChild.data
        vPrm=[]
        vs=plugSR_get.getElementsByTagName('vPrm')
        if len(vs)!=0:
            vs=vs[0].getElementsByTagName('v')
            for v in vs:
                vPrm.append(v.firstChild.data)
            
        presetNo=plugSR_get.getElementsByTagName('presetNo')[0].firstChild.data
        enable=plugSR_get.getElementsByTagName('enable')[0].firstChild.data
        bypass=plugSR_get.getElementsByTagName('bypass')[0].firstChild.data
        plugSR=[ID,name,sdkVer,nPrm,vPrm,presetNo,enable,bypass]
    else:
        plugSR=[]
    masterUnit.append(plugs)
    masterUnit.append(plugSR)
    masterUnit.append(master.getElementsByTagName('rLvl')[0].firstChild.data)
    masterUnit.append(master.getElementsByTagName('vol')[0].firstChild.data)
    mixer.append(masterUnit)
    #---------------------vsUnit--------------------------------------------------#
    vsUnits_get=mixer_get.getElementsByTagName('vsUnit')
    vsUnits=[]
    for vsunit in vsUnits_get:
        vsUnitParam=[]
        vsUnitParam.append(vsunit.getElementsByTagName('tNo')[0].firstChild.data)
        vsUnitParam.append(vsunit.getElementsByTagName('iGin')[0].firstChild.data)
        #plug
        plug_get=vsunit.getElementsByTagName('plug')
        plugs=[]
        
        if len(plug_get)!=0:
            for plug in plug_get:
                ID=plug.getElementsByTagName('id')[0].firstChild.data
                try:
                    name=plug.getElementsByTagName('name')[0].firstChild.data
                except AttributeError:
                    name=''
                    
                sdkVer=plug.getElementsByTagName('sdkVer')[0].firstChild.data
                nPrm=plug.getElementsByTagName('nPrm')[0].firstChild.data
                vPrm=[]
                vs=plug.getElementsByTagName('vPrm')
                if len(vs)!=0:
                    vs=vs[0].getElementsByTagName('v')
                    for v in vs:
                        vPrm.append(v.firstChild.data)
                    
                presetNo=plug.getElementsByTagName('presetNo')[0].firstChild.data
                enable=plug.getElementsByTagName('enable')[0].firstChild.data
                bypass=plug.getElementsByTagName('bypass')[0].firstChild.data
                plug_list=[ID,name,sdkVer,nPrm,vPrm,presetNo,enable,bypass]
                plugs.append(plug_list)
        vsUnitParam.append(plugs)
        vsUnitParam.append(vsunit.getElementsByTagName('sLvl')[0].firstChild.data)
        vsUnitParam.append(vsunit.getElementsByTagName('sEnable')[0].firstChild.data)
        vsUnitParam.append(vsunit.getElementsByTagName('m')[0].firstChild.data)
        vsUnitParam.append(vsunit.getElementsByTagName('s')[0].firstChild.data)
        vsUnitParam.append(vsunit.getElementsByTagName('pan')[0].firstChild.data)
        vsUnitParam.append(vsunit.getElementsByTagName('vol')[0].firstChild.data)
        vsUnits.append(vsUnitParam)
    mixer.append(vsUnits)
    #--------------------monoUnit---------------------------------------------------#
    vsunit=mixer_get.getElementsByTagName('monoUnit')[0]
    vsUnitParam=[]
    vsUnitParam.append(vsunit.getElementsByTagName('iGin')[0].firstChild.data)
    #plug
    plug_get=vsunit.getElementsByTagName('plug')
    plugs=[]
    if len(plug_get)!=0:
        for plug in plug_get:
            ID=plug.getElementsByTagName('id')[0].firstChild.data
            try:
                name=plug.getElementsByTagName('name')[0].firstChild.data
            except AttributeError:
                name=''
            sdkVer=plug.getElementsByTagName('sdkVer')[0].firstChild.data
            nPrm=plug.getElementsByTagName('nPrm')[0].firstChild.data
            vPrm=[]
            vs=plug.getElementsByTagName('vPrm')
            if len(vs)!=0:
                vs=vs[0].getElementsByTagName('v')
                for v in vs:
                    vPrm.append(v.firstChild.data)
                
            presetNo=plug.getElementsByTagName('presetNo')[0].firstChild.data
            enable=plug.getElementsByTagName('enable')[0].firstChild.data
            bypass=plug.getElementsByTagName('bypass')[0].firstChild.data
            plug_list=[ID,name,sdkVer,nPrm,vPrm,presetNo,enable,bypass]
            plugs.append(plug_list)
    vsUnitParam.append(plugs)
    vsUnitParam.append(vsunit.getElementsByTagName('sLvl')[0].firstChild.data)
    vsUnitParam.append(vsunit.getElementsByTagName('sEnable')[0].firstChild.data)
    vsUnitParam.append(vsunit.getElementsByTagName('m')[0].firstChild.data)
    vsUnitParam.append(vsunit.getElementsByTagName('s')[0].firstChild.data)
    vsUnitParam.append(vsunit.getElementsByTagName('pan')[0].firstChild.data)
    vsUnitParam.append(vsunit.getElementsByTagName('vol')[0].firstChild.data)
    mixer.append(vsUnitParam)
    #----------------------stUnit--------------------------------------------------------#
    vsunit=mixer_get.getElementsByTagName('stUnit')[0]
    vsUnitParam=[]
    vsUnitParam.append(vsunit.getElementsByTagName('iGin')[0].firstChild.data)
    #plug
    plug_get=vsunit.getElementsByTagName('plug')
    plugs=[]
    if len(plug_get)!=0:
        for plug in plug_get:
            ID=plug.getElementsByTagName('id')[0].firstChild.data
            try:
                name=plug.getElementsByTagName('name')[0].firstChild.data
            except AttributeError:
                name=''
            sdkVer=plug.getElementsByTagName('sdkVer')[0].firstChild.data
            nPrm=plug.getElementsByTagName('nPrm')[0].firstChild.data
            vPrm=[]
            vs=plug.getElementsByTagName('vPrm')
            if len(vs)!=0:
                vs=vs[0].getElementsByTagName('v')
                for v in vs:
                    vPrm.append(v.firstChild.data)
                
            presetNo=plug.getElementsByTagName('presetNo')[0].firstChild.data
            enable=plug.getElementsByTagName('enable')[0].firstChild.data
            bypass=plug.getElementsByTagName('bypass')[0].firstChild.data
            plug_list=[ID,name,sdkVer,nPrm,vPrm,presetNo,enable,bypass]
            plugs.append(plug_list)
    vsUnitParam.append(plugs)
    vsUnitParam.append(vsunit.getElementsByTagName('m')[0].firstChild.data)
    vsUnitParam.append(vsunit.getElementsByTagName('s')[0].firstChild.data)
    vsUnitParam.append(vsunit.getElementsByTagName('vol')[0].firstChild.data)
    mixer.append(vsUnitParam)
    vsq4_params.append(mixer)

    ####################  masterTracks  ###################################
    masterTrack_get=root.getElementsByTagName('masterTrack')[0]
    masterTrack=[]
    try:
        seqName=masterTrack_get.getElementsByTagName('seqName')[0].firstChild.data
    except AttributeError:
        seqName=''
    try:
        comment=masterTrack_get.getElementsByTagName('comment')[0].firstChild.data
    except AttributeError:
        comment=''        
    masterTrack.append(seqName)
    masterTrack.append(comment)
    masterTrack.append(masterTrack_get.getElementsByTagName('resolution')[0].firstChild.data)
    masterTrack.append(masterTrack_get.getElementsByTagName('preMeasure')[0].firstChild.data)
    timeSig=[]
    timeSig_get=masterTrack_get.getElementsByTagName('timeSig')
    for time in timeSig_get:
        m=time.getElementsByTagName('m')[0].firstChild.data
        nu=time.getElementsByTagName('nu')[0].firstChild.data
        de=time.getElementsByTagName('de')[0].firstChild.data
        timelist=[m,nu,de]
        timeSig.append(timelist)
    masterTrack.append(timeSig)
    tempo=[]
    tempo_get=masterTrack_get.getElementsByTagName('tempo')
    for time in tempo_get:
        t=time.getElementsByTagName('t')[0].firstChild.data
        v=time.getElementsByTagName('v')[0].firstChild.data
        tempolist=[t,v]
        tempo.append(tempolist)
    masterTrack.append(tempo)
    
    ##############   vsTrack ###############################################
    vstracks=root.getElementsByTagName('vsTrack')
    vsTrack=[]
    for vstrack in vstracks:
        #print('+')
        singelTrack=[]
        singelTrack.append(vstrack.getElementsByTagName('tNo')[0].firstChild.data)
        try:
            name=vstrack.getElementsByTagName('name')[0].firstChild.data
        except AttributeError:
            name=''
        try:
            comment=vstrack.getElementsByTagName('comment')[0].firstChild.data
        except AttributeError:
            comment=''
        
        singelTrack.append(name)
        singelTrack.append(comment)
        vsParts=[]
        vsparts=vstrack.getElementsByTagName('vsPart')
        for vspart in vsparts:
            vsPart=[]
            vsPart.append(vspart.getElementsByTagName('t')[0].firstChild.data)
            vsPart.append(vspart.getElementsByTagName('playTime')[0].firstChild.data)

            try:
                vsPartname=vspart.getElementsByTagName('name')[0].firstChild.data
            except AttributeError:
                vsPartname=''
            try:
                vsPartcomment=vspart.getElementsByTagName('comment')[0].firstChild.data
            except AttributeError:
                vsPartcomment=''
            
            vsPart.append(vsPartname)
            vsPart.append(vsPartcomment)
            splugs=vspart.getElementsByTagName('sPlug')[0]
            sPlug=[]
            sPlug.append(splugs.getElementsByTagName('id')[0].firstChild.data)
            sPlug.append(splugs.getElementsByTagName('name')[0].firstChild.data)
            sPlug.append(splugs.getElementsByTagName('version')[0].firstChild.data)
            vsPart.append(sPlug)
            pstyles=vspart.getElementsByTagName('pStyle')[0]
            v=pstyles.getElementsByTagName('v')
            pStyle=[v[0].firstChild.data,v[1].firstChild.data,v[2].firstChild.data,
                    v[3].firstChild.data,v[4].firstChild.data,v[5].firstChild.data,v[6].firstChild.data]
            vsPart.append(pStyle)
            singer_get=vspart.getElementsByTagName('singer')[0]
            singer=[]
            singer.append(singer_get.getElementsByTagName('t')[0].firstChild.data)
            singer.append(singer_get.getElementsByTagName('bs')[0].firstChild.data)
            singer.append(singer_get.getElementsByTagName('pc')[0].firstChild.data)
            vsPart.append(singer)
            #------------ VCC ----------------------------------------------------------------#
            ccs=vspart.getElementsByTagName('cc')
            VCCS=[]
            if len(ccs)!=0:
                for cc in ccs:
                    if cc.parentNode.tagName == 'vsPart':
                        cc_t=cc.getElementsByTagName('t')[0].firstChild.data  
                        cc_v_all=cc.getElementsByTagName('v')[0]
                        cc_v=cc_v_all.firstChild.data
                        cc_id=cc_v_all.getAttribute('id')
                        CC=[cc_t,cc_id,cc_v]
                        VCCS.append(CC)
            vsPart.append(VCCS)
            
            #-------------VNOTE---------------------------------------------------------------#

            notes=vspart.getElementsByTagName('note')
            VNOTES=[]
            if len(notes)!=0:
                for note in notes:
                    NOTE=[]
                    NOTE.append(note.getElementsByTagName('t')[0].firstChild.data)
                    NOTE.append(note.getElementsByTagName('dur')[0].firstChild.data)
                    NOTE.append(note.getElementsByTagName('n')[0].firstChild.data)
                    NOTE.append(note.getElementsByTagName('v')[0].firstChild.data)
                    NOTE.append(note.getElementsByTagName('y')[0].firstChild.data)
                    NOTE.append(note.getElementsByTagName('p')[0].firstChild.data)
                    Lock=note.getElementsByTagName('p')[0].getAttribute('lock')
                    nstyle=note.getElementsByTagName('nStyle')[0]
                    v=nstyle.getElementsByTagName('v')
                    NSTYLE=[v[0].firstChild.data,v[1].firstChild.data,
                            v[2].firstChild.data,v[3].firstChild.data,
                            v[4].firstChild.data,v[5].firstChild.data,
                            v[6].firstChild.data,v[7].firstChild.data,
                            v[8].firstChild.data]
                    
                    vibDep=[]
                    vibRate=[]
                    seqes=nstyle.getElementsByTagName('seq')
                    if len(seqes)!=0:
                        for seq in seqes:
                            CC=[]
                            ccs=seq.getElementsByTagName('cc')
                            if len(ccs)!=0:
                                for cc in ccs:
                                    cc_p=cc.getElementsByTagName('p')[0].firstChild.data
                                    cc_v=cc.getElementsByTagName('v')[0].firstChild.data
                                    CC.append([cc_p,cc_v])
                            if seq.getAttribute('id')=='vibDep':
                                vibDep=CC
                            else:
                                if seq.getAttribute('id')=='vibRate':
                                    vibRate=CC
                    NSTYLE.append(vibDep)
                    NSTYLE.append(vibRate)
                    NOTE.append(NSTYLE)
                    NOTE.append(Lock)
                    VNOTES.append(NOTE)
            
            vsPart.append(VNOTES)
            vsPart.append(vspart.getElementsByTagName('plane')[0].firstChild.data)
            vsParts.append(vsPart)
        singelTrack.append(vsParts)
        vsTrack.append(singelTrack)
    ###################  MonoTrack,stTrack,aux ###################
    monoTrack_get=root.getElementsByTagName('monoTrack')[0]
    monoTrack_waves=monoTrack_get.getElementsByTagName('wavPart')
    monoTrack=[]
    for wavepart in monoTrack_waves:
        t=wavepart.getElementsByTagName('t')[0].firstChild.data
        playTime=wavepart.getElementsByTagName('playTime')[0].firstChild.data
        name=wavepart.getElementsByTagName('name')[0].firstChild.data
        comment=wavepart.getElementsByTagName('comment')[0].firstChild.data
        fs=wavepart.getElementsByTagName('fs')[0].firstChild.data
        rs=wavepart.getElementsByTagName('rs')[0].firstChild.data
        nCh=wavepart.getElementsByTagName('nCh')[0].firstChild.data
        filePath=wavepart.getElementsByTagName('filePath')[0].firstChild.data
        wavelist=[t,playTime,name,comment,fs,rs,nCh,filePath]
        monoTrack.append(wavelist)
    #------------------stTrack---------------------------------#
    stTrack_get=root.getElementsByTagName('stTrack')[0]
    stTrack_waves=stTrack_get.getElementsByTagName('wavPart')
    stTrack=[]
    for wavepart in stTrack_waves:
        t=wavepart.getElementsByTagName('t')[0].firstChild.data
        playTime=wavepart.getElementsByTagName('playTime')[0].firstChild.data
        name=wavepart.getElementsByTagName('name')[0].firstChild.data
        comment=wavepart.getElementsByTagName('comment')[0].firstChild.data
        fs=wavepart.getElementsByTagName('fs')[0].firstChild.data
        rs=wavepart.getElementsByTagName('rs')[0].firstChild.data
        nCh=wavepart.getElementsByTagName('nCh')[0].firstChild.data
        filePath=wavepart.getElementsByTagName('filePath')[0].firstChild.data
        wavelist=[t,playTime,name,comment,fs,rs,nCh,filePath]
        stTrack.append(wavelist)
    #------------------aux---------------------------------#
    aux_get=root.getElementsByTagName('aux')[0]
    aux_id=aux_get.getElementsByTagName('id')[0].firstChild.data
    aux_content=aux_get.getElementsByTagName('content')[0].firstChild.data
    aux=[aux_id,aux_content]
    
            
    #test
    return VSQX4([vender,version,vVoiceTable,mixer,masterTrack,vsTrack,monoTrack,stTrack,aux])










    
