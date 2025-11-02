from bisect import bisect_left
import traceback
from typing import List, Iterator, Tuple, Union, Optional
import warnings
import os
import copy
import itertools
CHANGELINE=os.linesep

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
        self.wavPart:List[wavPart] = [wavPart(wav) for wav in wavPartList]
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
        self.wavPart:List[wavPart] = [wavPart(wav) for wav in wavPartList]
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
    def return_beat(self):
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
    def return_bpm(self):
        return str(float(self.v)/100)

class masterTrack():
    def __init__(self,params):
        [seqName,comment,resolution,preMeasure,TimeSigs,Tempos]=params
        self.seqName=seqName
        self.comment=comment
        self.resolution=resolution
        self.preMeasure=preMeasure
        self.timeSig:List[timeSig] = [timeSig(TimeSig) for TimeSig in TimeSigs]
        self.tempo:List[tempo] = [tempo(Tempo) for Tempo in Tempos]

    def return_bpm(self):
        if len(self.tempo)==1:
            return self.tempo[0].return_bpm()
        else:
            return self.tempo
    def return_beat(self):
        if len(self.timeSig)==1:
            return self.timeSig[0].return_beat()
        else:
            return self.timeSig
        
    def beat_to_t(self, bar: int, beat: int = 1, pos_in_bar: int = 0, pre_bar : bool = False) -> int:
        """
        输入小节、节拍和拍内位置，返回对应的绝对时间位置（t）
        
        重要假设：
        - bar: 小节索引，
        - beat: 拍子索引，
        - pos_in_bar: 拍子内的相对 tick 偏移量
        
        例如：计算 "第3小节第2拍第120个tick" 的位置，应调用：
        beat_to_t(bar=3, beat=2, pos_in_bar=120)
        """
        if bar <= 0:
            raise ValueError(f"Bar must be greater than 0, got {bar}.")
        if beat <= 0:
            raise ValueError(f"Beat must be greater than 0, got {beat}")
        if pos_in_bar < 0:
            raise ValueError(f"pos_in_bar must be greater than 0. got {pos_in_bar}")
        
        if not pre_bar:
            bar = bar + int(self.preMeasure) - 1
        beat = beat - 1
        
        normalization_length = 1920  # 1/1拍（全音符）对应的tick数
        beat_list = self.timeSig 

        total_t = 0
        
        # 遍历所有拍号变更
        for i in range(len(beat_list)):
            current_ts = beat_list[i]
            start_bar = int(current_ts.m)
            nu = int(current_ts.nu)
            de = int(current_ts.de)

            # 确定此拍号的结束小节（即下一个拍号的开始小节）
            next_start_bar = float('inf')
            if i + 1 < len(beat_list):
                next_start_bar = int(beat_list[i+1].m)
            
            ticks_per_bar = (normalization_length * nu) // de
            effective_start = start_bar 
            effective_end = min(next_start_bar, bar)
            num_bars = effective_end - effective_start
            
            if num_bars > 0:
                total_t += num_bars * ticks_per_bar
            if next_start_bar > bar:
                break
        active_ts = None
        for ts in reversed(beat_list):  # 反向遍历
            if int(ts.m) <= bar:
                active_ts = ts
                break
        nu = int(active_ts.nu)
        de = int(active_ts.de)
        ticks_per_beat = normalization_length // de
        total_t += beat * ticks_per_beat
        total_t += pos_in_bar
        
        return total_t

    def time_to_t(self, minute: int = 0, second: int = 0, millisecond: int = 0) -> int:
        """
        输入时间（分、秒、毫秒），返回对应的绝对时间位置（t）
        """
        target_total_ms = (minute * 60 + second) * 1000 + millisecond

        if len(self.tempo) == 0:
            raise myError("No tempo information available.")
        if int(tempo_events[0].t) != 0:
            raise myError("First tempo event must start at t=0.")
            
        tempo_events = sorted(self.tempo, key=lambda x: int(x.t))

        # PPQN (Pulses Per Quarter Note)
        ticks_per_quarter_note = 1920 / 4.0  # 480.0

        accumulated_ms = 0.0
        for i in range(len(tempo_events)):
            current_event = tempo_events[i]
            segment_start_t = int(current_event.t)
            current_v = float(current_event.v)
            if current_v <= 0:
                raise myError(f"Invalid tempo value {current_v} at t={segment_start_t}.")

            # bpm = beat (quarter notes) per minute
            bpm = current_v / 100.0
            
            # ticks_per_minute = bpm * ticks_per_quarter_note
            ticks_per_minute = bpm * ticks_per_quarter_note # e.g., 120 * 480 = 57600
            ticks_per_ms = ticks_per_minute / 60000.0 
            if ticks_per_ms == 0:
                raise myError(f"Tempo results in zero ticks/ms at t={segment_start_t}.")

            # --- 确定此 segment 的结束点 ---
            segment_end_t = float('inf')
            if i + 1 < len(tempo_events):
                segment_end_t = int(tempo_events[i+1].t)
                
            ticks_in_this_segment = segment_end_t - segment_start_t
            
            if ticks_in_this_segment <= 0:
                continue

            # --- 计算此 segment 占用的真实毫秒数 ---
            ms_in_this_segment = ticks_in_this_segment / ticks_per_ms
            
            # 检查目标时间是否落在这个 segment 内
            ms_needed_to_reach_target = target_total_ms - accumulated_ms
            
            if accumulated_ms + ms_in_this_segment >= target_total_ms:
                ticks_to_add = ms_needed_to_reach_target * ticks_per_ms
                
                final_t = segment_start_t + ticks_to_add
                return int(round(final_t))
            else:
                accumulated_ms += ms_in_this_segment
        
        ms_needed_after_last_event = target_total_ms - accumulated_ms
        ticks_to_add = ms_needed_after_last_event * ticks_per_ms
        final_t = segment_start_t + ticks_to_add
        
        return int(round(final_t))
        
    def t_to_beat(self, t: int, pre_bar: bool = False) -> Tuple[int, int, int]:
        """
        输入绝对时间位置 (t)，返回对应的小节、节拍和拍内偏移
        返回: (bar, beat, pos_in_bar)
        
        - bar: 小节索引 (从 0 开始)
        - beat: 拍子索引 (从 0 开始)
        - pos_in_bar: 拍内 tick 偏移 (从 0 开始)
        """
        normalization_length = 1920  # 1/1拍对应的tick数
        beat_list = sorted(self.timeSig, key=lambda x: int(x.m))

        if not beat_list or int(beat_list[0].m) != 0:
            raise myError("Invalid time signature definition at m=0.")
            
        if t < 0:
            return 0, 0, 0 # t=0 之前的位置

        total_ticks_so_far = 0

        for i in range(len(beat_list)):
            current_ts = beat_list[i]
            
            start_bar = int(current_ts.m)
            nu = int(current_ts.nu)
            de = int(current_ts.de)
            
            # 确定此拍号的结束小节
            next_start_bar = float('inf')
            if i + 1 < len(beat_list):
                next_start_bar = int(beat_list[i+1].m)
            
            # 计算此拍号下的 ticks
            ticks_per_bar = (normalization_length * nu) // de
            ticks_per_beat = normalization_length // de
            
            if ticks_per_bar <= 0 or ticks_per_beat <= 0:
                # 拍号无效 (例如 4/0)，跳过
                continue

            # 此拍号区间总共包含多少小节
            num_bars_in_segment = next_start_bar - start_bar
            
            # 此拍号区间总共包含多少 ticks
            ticks_in_segment = num_bars_in_segment * ticks_per_bar
            
            segment_end_ticks = total_ticks_so_far + ticks_in_segment
            
            # 注意: t 恰好等于 segment_end_ticks 时，属于下一个区间)
            if t < segment_end_ticks:
                ticks_into_this_segment = t - total_ticks_so_far
                
                
                # 计算这个偏移量等于多少个小节
                num_bars_into_segment = ticks_into_this_segment // ticks_per_bar
                
                # 计算最终的小节索引
                bar = start_bar + num_bars_into_segment
                # 计算在那个小节内的 tick 偏移
                ticks_into_this_bar = ticks_into_this_segment % ticks_per_bar
                
                # 计算最终的节拍索引
                beat = ticks_into_this_bar // ticks_per_beat
                
                # 计算最终的拍内偏移
                pos_in_bar = ticks_into_this_bar % ticks_per_beat

                if not pre_bar:
                    bar = int(bar) - int(self.preMeasure) + 1
                
                return int(bar), int(beat) + 1, int(pos_in_bar)
            
            # t 在这个区间之后，累加这个区间的总 ticks，继续循环
            total_ticks_so_far = segment_end_ticks

        # (这部分代码理论上不应被执行)  
        # 如果 t 超出了所有定义的拍号（不应发生，因为最后一个区间是 inf）
        # 但为防万一，返回一个基于最后一个拍号的计算
        
        last_ts = beat_list[-1]
        start_bar = int(last_ts.m)
        ticks_per_bar = (normalization_length * int(last_ts.nu)) // int(last_ts.de)
        ticks_per_beat = normalization_length // int(last_ts.de)
        
        ticks_into_this_segment = t - total_ticks_so_far
        num_bars_into_segment = ticks_into_this_segment // ticks_per_bar
        bar = start_bar + num_bars_into_segment
        ticks_into_this_bar = ticks_into_this_segment % ticks_per_bar
        beat = ticks_into_this_bar // ticks_per_beat
        pos_in_bar = ticks_into_this_bar % ticks_per_beat

        if not pre_bar:
            bar = int(bar) - int(self.preMeasure) + 1
        
        return int(bar), int(beat) + 1, int(pos_in_bar)    

    def t_to_time(self, t: int) -> Tuple[int, int, int]:
        """
        输入绝对时间位置 (t)，返回对应的真实时间（分、秒、毫秒）
        返回: (minute, second, millisecond)
        """
        target_t = t
        
        if len(self.tempo) == 0:
            raise myError("No tempo information available.")

        tempo_events = sorted(self.tempo, key=lambda x: int(x.t))
        
        # 1/4 (四分音符) = 1920 / 4 = 480 ticks
        ticks_per_quarter_note = 1920 / 4.0  # 480.0

        # 确保 t=0 时有 tempo
        if int(tempo_events[0].t) != 0:
            raise myError("First tempo event must start at t=0.")

        if target_t < 0:
            return 0, 0, 0

        accumulated_ms = 0.0

        for i in range(len(tempo_events)):
            current_event = tempo_events[i]
            segment_start_t = int(current_event.t)
            
            current_v = float(current_event.v)
            if current_v <= 0:
                raise myError(f"Invalid tempo value {current_v} at t={segment_start_t}.")

            # --- 计算此 segment 的 ms <-> ticks 转换率 ---
            
            # 1. BPM
            bpm = current_v / 100.0
            
            # 2. Ticks per Minute
            ticks_per_minute = bpm * ticks_per_quarter_note
            
            # 3. Ticks per Millisecond
            ticks_per_ms = ticks_per_minute / 60000.0
            
            if ticks_per_ms == 0:
                continue
                
            # 4. Milliseconds per Tick (这个更易于计算)
            ms_per_tick = 1.0 / ticks_per_ms # 60000.0 / ticks_per_minute

            # --- 确定此 segment 的结束点 ---
            segment_end_t = float('inf')
            if i + 1 < len(tempo_events):
                segment_end_t = int(tempo_events[i+1].t)
                
            ticks_in_this_segment = segment_end_t - segment_start_t
            
            # 检查 target_t 是否落在这个 segment 内
            # (注意: t 恰好等于 segment_end_t 时，属于下一个区间)
            if target_t < segment_end_t:
                ticks_into_this_segment = target_t - segment_start_t
                
                # 将这个 tick 偏移转换为毫秒
                ms_to_add = ticks_into_this_segment * ms_per_tick
                
                # 得到最终的总毫秒数
                total_ms = accumulated_ms + ms_to_add
                
                # --- 分解 total_ms 为 (min, sec, ms) ---
                
                # 四舍五入到最近的毫秒
                total_ms_int = int(round(total_ms))
                
                total_seconds = total_ms_int // 1000
                millisecond = total_ms_int % 1000
                
                minute = total_seconds // 60
                second = total_seconds % 60
                
                return int(minute), int(second), int(millisecond)
            
            # target_t 在这个区间之后，累加这个区间的总毫秒数，继续循环
            if ticks_in_this_segment > 0:
                ms_in_this_segment = ticks_in_this_segment * ms_per_tick
                accumulated_ms += ms_in_this_segment
        
        # (这部分代码理论上不应被执行)
        # 如果 t 超出了所有定义的 tempo（不应发生，因为最后一个区间是 inf）
        # 但为防万一，我们返回一个基于最后一个 tempo 的计算
        
        last_event = tempo_events[-1]
        segment_start_t = int(last_event.t)
        ms_per_tick = 60000.0 / ((float(last_event.v) / 100.0) * ticks_per_quarter_note)
        
        ticks_into_this_segment = target_t - segment_start_t
        ms_to_add = ticks_into_this_segment * ms_per_tick
        total_ms = accumulated_ms + ms_to_add
        
        total_ms_int = int(round(total_ms))
        total_seconds = total_ms_int // 1000
        millisecond = total_ms_int % 1000
        minute = total_seconds // 60
        second = total_seconds % 60
                
        return int(minute), int(second), int(millisecond)


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
            self.plugs = []
        else:
            self.plugs:List[plug] = [plug(plug_param) for plug_param in plugs]
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
            self.plugs:List[plug] = []
        else:
            self.plugs:List[plug] = [plug(plug_param) for plug_param in plugs]
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
            self.plugs:List[plug] = []
        else:
            self.plugs:List[plug] = [plug(plug_param) for plug_param in plugs]
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
            self.plugs:List[plug] = []
        else:
            self.plugs:List[plug] = [plug(plug_param) for plug_param in plugs]
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
        if len(vsUnits_param)!=0:
            self.vsUnits:List[vsUnit] = [vsUnit(vsUnit_param) for vsUnit_param in vsUnits_param]
        else:
            self.vsUnits:List[vsUnit] = []

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
class SeqVibDep():
    def __init__(self,seqccs_param):
        #seqcc_param=param
        if len(seqccs_param)==0:
            self.seqcc_param:List[seqcc] = []
        else:
            self.seqcc_param:List[seqcc] = [seqcc(seqcc_param) for seqcc_param in seqccs_param]
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

class SeqVibRate():
    def __init__(self,seqccs_param):
        #seqcc_param=param
        if len(seqccs_param)==0:
            self.seqcc_param:List[seqcc] = []
        else:
            self.seqcc_param:List[seqcc] = [seqcc(seqcc_param) for seqcc_param in seqccs_param]
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
        self.vibDep=SeqVibDep(vibDep)
        self.vibRate=SeqVibRate(vibRate)
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
        
    def __lt__(self, other):
        try:
            return int(self.t) < int(other.t)
        except (AttributeError, ValueError, TypeError):
            return NotImplemented
        
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
    
    @classmethod
    def check_int(cls, value, name, minv, maxv=None):
        try:
            iv=int(value)
        except ValueError:
            raise ValueError(f'{name} must be an integer or can be converted to an integer, but got {value}')
        if maxv is None:
            if iv<minv:
                raise ValueError(f'{name} must be >= {minv}, but got {iv}')
        else:
            if iv<minv or iv>maxv:
                raise ValueError(f'{name} must be between {minv} and {maxv}, but got {iv}')

    @classmethod
    def check_all_val(cls, t='0',dur='1920',n='60',v='64',y='a',p='a',
                    accent='50',bendDep='8',bendLen='0',decay='50',
                    fallPort='0',opening='127',risePort='0',
                    vibLen='0',vibType='0',vibDep:list=[],vibRate:list=[]):
        cls.check_int(value=t,name='t',minv=0)
        cls.check_int(value=dur,name='dur',minv=1)
        cls.check_int(value=n,name='n',minv=0,maxv=127)
        cls.check_int(value=v,name='v',minv=0,maxv=127)
        cls.check_int(value=accent,name='accent',minv=0,maxv=127)
        cls.check_int(value=bendDep,name='bendDep',minv=0,maxv=127)
        cls.check_int(value=bendLen,name='bendLen',minv=0,maxv=127)
        cls.check_int(value=decay,name='decay',minv=0,maxv=127)
        cls.check_int(value=fallPort,name='fallPort',minv=0,maxv=1)
        cls.check_int(value=opening,name='opening',minv=0,maxv=127)
        cls.check_int(value=risePort,name='risePort',minv=0,maxv=1)
        cls.check_int(value=vibLen,name='vibLen',minv=0,maxv=127)
        cls.check_int(value=vibType,name='vibType',minv=0,maxv=127)
        if not isinstance(vibDep,list):
            raise TypeError(f'vibDep must be a list, but got {type(vibDep)}')
        for i in vibDep:
            cls.check_int(value=i,name='vibDep',minv=0,maxv=127)
        if not isinstance(vibRate,list):
            raise TypeError(f'vibRate must be a list, but got {type(vibRate)}')
        for i in vibRate:
            cls.check_int(value=i,name='vibRate',minv=0,maxv=127)
        
      
    @classmethod
    def create(cls, t='0',dur='1920',n='60',v='64',y='a',p='a',
                    accent='50',bendDep='8',bendLen='0',decay='50',
                    fallPort='0',opening='127',risePort='0',
                    vibLen='0',vibType='0',vibDep:list=[],vibRate:list=[],
                    lock='') -> 'VNOTE':
        ## data checking:
        cls.check_all_val(t,dur,n,v,y,p,
                    accent,bendDep,bendLen,decay,
                    fallPort,opening,risePort,vibLen,vibType,vibDep,vibRate)

        nstyle = [accent,bendDep,bendLen,decay,fallPort,opening,risePort,vibLen,vibType,vibDep,vibRate]
        params = [t, dur, n, v, y, p, nstyle, lock]
        return cls(params)

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
    def __lt__(self, other):
        try:
            return int(self.t) < int(other.t)
        except (AttributeError, ValueError, TypeError):
            return NotImplemented
    @classmethod
    def change_vcc_id(cls, ID):
        allID=['D','B','R','C','G','T','X','W','P','S',
               'd',b'','r','c','g','t','x','w','p','s',
               'DYN','BRN','BRI','CLE','GEN','POR','XSY','GWL','PIT','PBS',
               'dyn','brn','bri','cle','gen','por','xsy','gwl','pit','pbs']
        if ID not in allID:
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
    
    @classmethod
    def check_int(cls, value, name, minv, maxv=None):
        try:
            iv=int(value)
        except ValueError:
            raise ValueError(f'{name} must be an integer or can be converted to an integer, but got {value}')
        if maxv is None:
            if iv<minv:
                raise ValueError(f'{name} must be >= {minv}, but got {iv}')
        else:
            if iv<minv or iv>maxv:
                raise ValueError(f'{name} must be between {minv} and {maxv}, but got {iv}')
    @classmethod
    def create(cls, t='0',ID='DYN',v='64') -> 'VCC':
        ## data checking:

        cls.check_int(value=t,name='t',minv=0)
        ID_checked=cls.change_vcc_id(ID)
        if not ID_checked:
            raise ValueError(f'ID must be one of DYN,BRN,BRI,CLE,GEN,POR,XSY,GWL,PIT,PBS (case insensitive), but got {ID}')
        if ID_checked in ['D','B','R','C','G','T','X','W']:
            cls.check_int(value=v,name='v',minv=0,maxv=127)
        if ID_checked in ['P']:
            cls.check_int(value=v,name='v',minv=-8192,maxv=8191)
        if ID_checked in ['S']:
            cls.check_int(value=v,name='v',minv=0,maxv=24)

        params = [t, ID_checked, v]
        return cls(params)


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
        self.VCC: List[VCC] = [VCC(cc) for cc in ccs]
        self.VNote: List[VNOTE] = [VNOTE(note) for note in notes]
        
    def return_param(self):
        return [self.t,self.playTime,self.name,self.comment,self.sPlug,self.pStyle,self.singer,self.VCC,self.VNote,self.plane]
    
    ## VNote和VCC的CRUD操作函数：

    def insert_vnote(self,vnote:Union[VNOTE,None]=None, t='0',dur='1920',n='60',v='64',y='a',p='a',
                    accent='50',bendDep='8',bendLen='0',decay='50',
                    fallPort='0',opening='127',risePort='0',
                    vibLen='0',vibType='0',vibDep=[],vibRate=[],
                    lock=''):
        """插入一个音符。根据所给的t自动插入到正确的位置。可以输入VNOTE类的实例。若不提供，则根据其他参数创建一个新的音符并插入。"""
        if vnote is None:
            VNOTE.check_int(value=t,name='t',minv=0)
            VNOTE.check_int(value=dur,name='dur',minv=0)
        t_end = int(t) + int(dur) if vnote is None else int(vnote.t) + int(vnote.dur)
        if t_end > int(self.playTime):
            raise ValueError(f"Insertion Error: Note end time {t_end} exceeds part playTime {self.playTime}.")

        if vnote is None:
            VNOTE.create(t,dur,n,v,y,p,
                    accent,bendDep,bendLen,decay,
                    fallPort,opening,risePort,vibLen,vibType,vibDep,vibRate,
                    lock)
            
        t_values_as_int = [int(vn.t) for vn in self.VNote]
        idx = bisect_left(t_values_as_int, int(vnote.t))
        if idx < len(self.VNote):
            next_vnote = self.VNote[idx]
            new_note_end_time = int(vnote.t) + int(vnote.dur)
            next_note_start_time = int(next_vnote.t)
            if new_note_end_time > next_note_start_time:
                raise myError(
                    f"Insertion Error: New note (t={vnote.t}, dur={vnote.dur}) with end time {new_note_end_time} "
                    f"overlaps with the next note (t={next_vnote.t})."
                )
        if idx > 0:
            prev_vnote = self.VNote[idx - 1]
            prev_note_end_time = int(prev_vnote.t) + int(prev_vnote.dur)
            if int(vnote.t) < prev_note_end_time:
                raise myError(
                    f"Insertion Error: New note (t={vnote.t}) overlaps with the previous note (t={prev_vnote.t}, dur={prev_vnote.dur}) "
                    f"which ends at {prev_note_end_time}."
                )

        self.VNote.insert(idx, vnote)

    def insert_vcc(self, vcc: Union[VCC , None] = None, ID="D", value="64", t="0"):
        """插入一个参数点。根据所给的t自动插入到正确的位置"""
        if vcc is None:
            VCC.check_int(value=t,name='t',minv=0)

        t=int(t) if vcc is None else int(vcc.t)

        if t > int(self.playTime):
            raise ValueError(f"Insertion Error: VCC time {t} exceeds part playTime {self.playTime}.")
        if vcc is None:
            vcc = VCC.create(t, ID, value)

        vcc_searched = self.search_vcc(t=vcc.t, ID=vcc.ID, value=vcc.v)
        for existing_vcc in vcc_searched:
            del self.VCC[self.VCC.index(existing_vcc)]

        t_values_as_int = [int(vc.t) for vc in self.VCC]
        idx = bisect_left(t_values_as_int, int(vcc.t))
        self.VCC.insert(idx, vcc)

    def search_vnote(self, t: Union[str, int, None] = None,
                    dur: Union[str, int, None] = None,
                    n: Union[str, int, None] = None,
                    v: Union[str, int, None] = None,
                    y: Union[str, None] = None,
                    p: Union[str, None] = None,
                    accent: Union[str, int, None] = None,
                    bendDep: Union[str, int, None] = None,
                    bendLen: Union[str, int, None] = None,
                    decay: Union[str, int, None] = None,
                    fallPort: Union[str, int, None] = None,
                    opening: Union[str, int, None] = None,
                    risePort: Union[str, int, None] = None,
                    vibLen: Union[str, int, None] = None,
                    vibType: Union[str, int, None] = None,
                    vibDep: Union[List[int], List[str], None] = None,
                    vibRate: Union[List[int], List[str], None] = None
                    ) -> List[VNOTE]:
        """搜索符合条件的音符，返回一个列表。可以根据多个条件进行搜索，任意一个或多个条件均可。
        函数会返回所有符合条件的音符的列表。"""
        if t is not None:
            VNOTE.check_int(value=t,name='t',minv=0)
            t = int(t)
        if dur is not None:
            VNOTE.check_int(value=dur,name='dur',minv=1)
            dur = int(dur)
        if n is not None:
            VNOTE.check_int(value=n,name='n',minv=0,maxv=127)
            n = int(n)
        if v is not None:
            VNOTE.check_int(value=v,name='v',minv=0,maxv=127)
            v = int(v)
        if accent is not None:
            VNOTE.check_int(value=accent,name='accent',minv=0,maxv=127)
            accent = int(accent)
        if bendDep is not None:
            VNOTE.check_int(value=bendDep,name='bendDep',minv=0,maxv=127)
            bendDep = int(bendDep)
        if bendLen is not None:
            VNOTE.check_int(value=bendLen,name='bendLen',minv=0,maxv=127)
            bendLen = int(bendLen)
        if decay is not None:
            VNOTE.check_int(value=decay,name='decay',minv=0,maxv=127)
            decay = int(decay)
        if fallPort is not None:
            VNOTE.check_int(value=fallPort,name='fallPort',minv=0,maxv=1)
            fallPort = int(fallPort)
        if opening is not None:
            VNOTE.check_int(value=opening,name='opening',minv=0,maxv=127)
            opening = int(opening)
        if risePort is not None:
            VNOTE.check_int(value=risePort,name='risePort',minv=0,maxv=1)
            risePort = int(risePort)
        if vibLen is not None:
            VNOTE.check_int(value=vibLen,name='vibLen',minv=0,maxv=127)
            vibLen = int(vibLen)
        if vibType is not None:
            VNOTE.check_int(value=vibType,name='vibType',minv=0,maxv=127)
            vibType = int(vibType)
        if vibDep is not None:
            if not isinstance(vibDep,list):
                raise TypeError(f'vibDep must be a list, but got {type(vibDep)}')
            for dep in vibDep:
                VNOTE.check_int(value=dep,name='vibDep',minv=0,maxv=127)
        if vibRate is not None:
            if not isinstance(vibRate,list):
                raise TypeError(f'vibRate must be a list, but got {type(vibRate)}')
            for rate in vibRate:
        
                VNOTE.check_int(value=rate,name='vibRate',minv=0,maxv=127)
        """result: List[VNOTE] = []
        for note in self.VNote:
            if (t is None or int(note.t) == t) and \
               (dur is None or int(note.dur) == dur) and \
               (n is None or int(note.n) == n) and \
                (v is None or int(note.v) == v) and \
                (y is None or note.y == y) and \
                (p is None or note.p == p) and \
                (accent is None or int(note.nStyle.accent) == accent) and \
                (bendDep is None or int(note.nStyle.bendDep) == bendDep) and \
                (bendLen is None or int(note.nStyle.bendLen) == bendLen) and \
                (decay is None or int(note.nStyle.decay) == decay) and \
                (fallPort is None or int(note.nStyle.fallPort) == fallPort) and \
                (opening is None or int(note.nStyle.opening) == opening) and \
                (risePort is None or int(note.nStyle.risePort) == risePort) and \
                (vibLen is None or int(note.nStyle.vibLen) == vibLen) and \
                (vibType is None or int(note.nStyle.vibType) == vibType):
                if vibDep is not None:
                    if len(vibDep) == len(note.nStyle.vibDep.seqcc_param):
                        note_vibDep = [int(val.p) for val in note.nStyle.vibDep.seqcc_param]
                        search_vibDep = [int(val) for val in vibDep]
                        if note_vibDep != search_vibDep:
                            continue
                if vibRate is not None:
                    if len(vibRate) == len(note.nStyle.vibRate.seqcc_param):
                        note_vibRate = [int(val.p) for val in note.nStyle.vibRate.seqcc_param]
                        search_vibRate = [int(val) for val in vibRate]
                        if note_vibRate != search_vibRate:
                            continue

                result.append(note)"""
        
        search_vibDep = [int(val) for val in vibDep] if vibDep is not None else None
        search_vibRate = [int(val) for val in vibRate] if vibRate is not None else None
        result = [
            note for note in self.VNote
            if (t is None or int(note.t) == t) and
            (dur is None or int(note.dur) == dur) and
            (n is None or int(note.n) == n) and
            (v is None or int(note.v) == v) and
            (y is None or note.y == y) and
            (p is None or note.p == p) and
            (accent is None or int(note.nStyle.accent) == accent) and
            (bendDep is None or int(note.nStyle.bendDep) == bendDep) and
            (bendLen is None or int(note.nStyle.bendLen) == bendLen) and
            (decay is None or int(note.nStyle.decay) == decay) and
            (fallPort is None or int(note.nStyle.fallPort) == fallPort) and
            (opening is None or int(note.nStyle.opening) == opening) and
            (risePort is None or int(note.nStyle.risePort) == risePort) and
            (vibLen is None or int(note.nStyle.vibLen) == vibLen) and
            (vibType is None or int(note.nStyle.vibType) == vibType) and
            (search_vibDep is None or (
                len(search_vibDep) == len(note.nStyle.vibDep.seqcc_param) and
                [int(val.p) for val in note.nStyle.vibDep.seqcc_param] == search_vibDep
            )) and
            (search_vibRate is None or (
                len(search_vibRate) == len(note.nStyle.vibRate.seqcc_param) and
                [int(val.p) for val in note.nStyle.vibRate.seqcc_param] == search_vibRate
            ))
        ]
        return result

    def search_vcc(self, t: Union[str, int, None]=None, ID: Union[str, None]=None, value: Union[str, int, None]=None) -> List[VCC]:
        """搜索符合条件的VCC点，返回一个列表。可以根据t, ID, value进行搜索，任意一个或多个条件均可。
        函数会返回所有符合条件的VCC点的列表。
        :param t: VCC点的时间，可以是字符串或整数
        :param ID: VCC点的ID，可以是字符串
        :param value: VCC点的值，可以是字符串或整数
        :return: 符合条件的VCC点列表
        """
        if t is not None:
            VCC.check_int(value=t,name='t',minv=0)
            t = int(t)
        if value is not None:
            VCC.check_int(value=value,name='value',minv=0)
            value = int(value)
        if ID is not None:
            ID_checked = VCC.change_vcc_id(ID)
            if not ID_checked:
                raise ValueError(f'ID must be one of DYN,BRN,BRI,CLE,GEN,POR,XSY,GWL,PIT,PBS (case insensitive), but got {ID}')
            ID = ID_checked
        # result: List[VCC] = []
        # for vcc in self.VCC:
        #     if (t is None or int(vcc.t) == t) and (ID is None or vcc.ID == ID) and (value is None or int(vcc.v) == value):
        #         result.append(vcc)
        result = [vcc for vcc in self.VCC if
                  (t is None or int(vcc.t) == t) and
                  (ID is None or vcc.ID == ID) and
                  (value is None or int(vcc.v) == value)]
        return result
    
    def get_vnote_from_time_range(self, start_time: Union[str, int, None]=None, end_time: Union[str, int, None]=None) -> List[VNOTE]:
        """获取指定时间范围内的音符列表"""
        if start_time is not None:
            VNOTE.check_int(value=start_time,name='start_time',minv=0)
            start_time = int(start_time)
        if end_time is not None:
            VNOTE.check_int(value=end_time,name='end_time',minv=0)
            end_time = int(end_time)
        result = [note for note in self.VNote
                  if (start_time is None or int(note.t) >= start_time) and
                  (end_time is None or int(note.t) + int(note.dur) <= end_time)]
        return result
    
    def get_vcc_from_time_range(self, start_time: Union[str, int, None]=None, end_time: Union[str, int, None]=None) -> List[VCC]:
        """获取指定时间范围内的VCC点列表"""
        if start_time is not None:
            VCC.check_int(value=start_time,name='start_time',minv=0)
            start_time = int(start_time)
        if end_time is not None:
            VCC.check_int(value=end_time,name='end_time',minv=0)
            end_time = int(end_time)
        result = [vcc for vcc in self.VCC
                  if (start_time is None or int(vcc.t) >= start_time) and
                  (end_time is None or int(vcc.t) <= end_time)]
        return result
    
    def cover_period_vnote(self, new_vnotes: List[VNOTE]) -> None:
        """用新的音符列表覆盖指定时间段内的音符"""
        sorted_new_vnotes = sorted(new_vnotes)
        if len(sorted_new_vnotes) == 0:
            return
        start_time = int(sorted_new_vnotes[0].t)
        end_time = int(sorted_new_vnotes[-1].t) + int(sorted_new_vnotes[-1].dur)
        self.VNote = [note for note in self.VNote if not (int(note.t) + int(note.dur) >= start_time and (int(note.t)) <= end_time)]
        for new_note in sorted_new_vnotes:
            self.insert_vnote(vnote=new_note)
        self.VNote = sorted(self.VNote)

    def cover_period_vcc(self, new_vccs: List[VCC]) -> None:
        """用新的VCC列表覆盖指定时间段内的VCC点"""
        sorted_new_vccs = sorted(new_vccs)
        if len(sorted_new_vccs) == 0:
            return
        start_time = int(sorted_new_vccs[0].t)
        end_time = int(sorted_new_vccs[-1].t)
        self.VCC = [vcc for vcc in self.VCC if not (int(vcc.t) >= start_time and int(vcc.t) <= end_time)]
        for new_vcc in sorted_new_vccs:
            self.insert_vcc(vcc=new_vcc)
        self.VCC = sorted(self.VCC)

    def delete_vnote(self, vnote: VNOTE) -> None:
        """删除指定的音符实例"""
        try:
            self.VNote.remove(vnote)
        except ValueError:
            raise ValueError("The specified VNOTE instance is not found in this vsPart.")
    
    def delete_vcc(self, vcc: VCC) -> None:
        """删除指定的VCC实例"""
        try:
            self.VCC.remove(vcc)
        except ValueError:
            raise ValueError("The specified VCC instance is not found in this vsPart.")

    ##
      
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
        self.vsPart:List[vsPart] = [vsPart(vspart) for vspart in vsParts]
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
        all_note = list(itertools.chain.from_iterable(part.VNote for part in self.vsPart))
        return all_note
    
    def return_all_cc(self):
        all_cc = list(itertools.chain.from_iterable(part.VCC for part in self.vsPart))
        return all_cc
     
    def create_vspart(self,t='0',playTime='1920',name='NewPart',
                      comment='New Musical Part',sPlugs=[],
                      pStyles=[],singers=[],ccs=[],notes=[],plane=0):
        if sPlugs==[] or pStyles==[] or singers==[]:
            try:
                vsPartInfo=self.vsPart[0]
            except IndexError:
                raise NotImplementedError("""create vspart from zero is not implemented because cannot find the information of singers.
                                Try to create a part from Vocaloid or giving the params of sPlugs, bStyles and singers""")
            else:
                if sPlugs==[]:
                    sPlugs=vsPartInfo.sPlug.return_param()
                if pStyles==[]:
                    pStyles=vsPartInfo.pStyle.return_param()
                if singers==[]:
                    singers=vsPartInfo.singer.return_param()
        vspart=[t,playTime,name,comment,sPlugs,pStyles,singers,ccs,notes,plane]
        self.vsPart.append(vsPart(vspart))
        #self.vsPart=sorted(self.vsPart)
    
    ## VNote 和 VCC的CRUD操作函数。t均为绝对时间
    def insert_note(self, vnote: Union[VNOTE, None] = None, t='0', dur='1920', n='60', v='64', y='a', p='a',
                    accent='50',bendDep='8',bendLen='0',decay='50',
                    fallPort='0',opening='127',risePort='0',
                    vibLen='0',vibType='0',vibDep:list=[],vibRate:list=[],
                    lock=''):
        """
        创建一个音符并插入到合适的Part中。**注意**: t 为音符的开始绝对时间，不能小于第一个VSPart的开始时间，且音符必须完全包含在某个VSPart内，否则会报错。
        可以输入VNOTE类的实例。若不提供，则根据其他参数创建一个新的音符并插入。
        :param t: 音符的开始绝对时间
        :param dur: 音符的持续时间
        :param n: 音符的音高
        :param v: 音符的音量
        :param y: 音符的音色
        :param p: 音符的音阶
        :param accent: 音符的重音
        :param bendDep: 音符的弯音深度
        :param bendLen: 音符的弯音长度
        :param decay: 音符的衰减
        :param fallPort: 音符的下滑音量
        :param opening: 音符的开口度
        :param risePort: 音符的上滑音量
        :param vibLen: 音符的颤音长度
        :param vibType: 音符的颤音类型
        :param vibDep: 音符的颤音深度
        :param vibRate: 音符的颤音速率
        :param lock: 音符的锁定状态
        """
        if vnote is not None and not isinstance(vnote, VNOTE):
            raise TypeError("vnote must be an instance of VNOTE class or None")
        if vnote is not None:
            t_abs = int(vnote.t)
            dur = int(vnote.dur)        
        else:
            VNOTE.check_int(value=t,name='t',minv=0)
            VNOTE.check_int(value=dur,name='dur',minv=0)
            t_abs = int(t)
            dur = int(dur)
            
        for part in self.vsPart:
            if int(part.t)<=int(t_abs) and int(part.t)+int(part.playTime)>=int(t_abs)+int(dur):
                if vnote is None:
                    part.insert_vnote(None,str(int(t)-int(part.t)),dur,n,v,y,p,
                                 accent,bendDep,bendLen,decay,fallPort,opening,
                                 risePort,vibLen,vibType,vibDep,vibRate,lock)
                
                else:
                    vnote.t=str(int(vnote.t)-int(part.t))
                    part.insert_vnote(vnote)
                return True
        raise myError('cannot find a fitting vspart.Try to using create_vspart to create a fitting vsPart')

    def insert_cc(self, vcc: Union[VCC, None] = None, typ='D', value='64', t='0'):
        if vcc is not None:
            t = int(vcc.t)
        else:
            VCC.check_int(value=t,name='t',minv=0)
            t = int(t)

        for part in self.vsPart:
            if int(part.t)<=int(t) and int(part.t)+int(part.playTime)>=int(t):
                if vcc is None:
                    part.insert_vcc(vcc=None,ID=typ,value=value,t=str(int(t)-int(part.t)))
                else:
                    vcc.t = str(int(vcc.t) - int(part.t))
                    part.insert_vcc(vcc=vcc)
                return True
        raise myError('cannot find a fitting vspart.Try to using create_vspart to create a fitting vsPart')
           
    def search_note(self, t: Union[str, int, None] = None,
                    dur: Union[str, int, None] = None,
                    n: Union[str, int, None] = None,
                    v: Union[str, int, None] = None,
                    y: Union[str, None] = None,
                    p: Union[str, None] =None,
                    accent: Union[str, int, None] = None,
                    bendDep: Union[str, int, None] = None,
                    bendLen: Union[str, int, None] = None,
                    decay: Union[str, int, None] = None,
                    fallPort: Union[str, int, None] = None,
                    opening: Union[str, int, None] = None,
                    risePort: Union[str, int, None] = None,
                    vibLen: Union[str, int, None] = None,
                    vibType: Union[str, int, None] = None,
                    vibDep: Union[List[int], List[str], None] = None,
                    vibRate: Union[List[int], List[str], None] = None
                    ) -> List[VNOTE]:
        """搜索符合条件的音符，返回一个列表。可以根据多个条件进行搜索，任意一个或多个条件均可。
        函数会返回所有符合条件的音符的列表。**注意**: t参数为音符的绝对时间。
        """
        t_abs: Union[int, None] = None
        if t is not None:
            VNOTE.check_int(value=t, name='t', minv=0)
            t_abs = int(t)

        def _get_notes_from_parts() -> Iterator[List[VNOTE]]:
            for part in self.vsPart:
                part_t_abs = int(part.t)
                t_in_part: Union[int, None] = None
                if t_abs is not None:
                    part_end_time = part_t_abs + int(part.playTime)
                    if t_abs < part_t_abs or t_abs > part_end_time:
                        continue # t 不在这个 part 内，跳过整个 part
                    t_in_part = t_abs - part_t_abs
                part_result = part.search_vnote(t=t_in_part, 
                                                dur=dur, n=n, v=v, y=y, p=p,
                                                accent=accent, bendDep=bendDep,bendLen=bendLen, 
                                                decay=decay,fallPort=fallPort, opening=opening, 
                                                risePort=risePort, vibLen=vibLen, vibType=vibType, 
                                                vibDep=vibDep,vibRate=vibRate)
                yield part_result 

        return list(itertools.chain.from_iterable(_get_notes_from_parts()))

    def search_cc(self, t: Union[str, int, None]=None, ID: Union[str, None]=None, value: Union[str, int, None]=None) -> List[VCC]:
        """搜索符合条件的VCC点，返回一个列表。可以根据t, ID, value进行搜索，任意一个或多个条件均可。**注意**: t参数为VCC点的绝对时间。
        函数会返回所有符合条件的VCC点的列表。
        :param t: VCC点的时间，可以是字符串或整数
        :param ID: VCC点的ID，可以是字符串
        :param value: VCC点的值，可以是字符串或整数
        :return: 符合条件的VCC点列表
        """
        t_abs: Union[int, None] = None
        if t is not None:
            VCC.check_int(value=t,name='t',minv=0)
            t_abs = int(t)

        def _get_vccs_from_parts() -> Iterator[List[VCC]]:
            for part in self.vsPart:
                part_t_abs = int(part.t)
                t_in_part: Union[int, None] = None
                if t_abs is not None:
                    part_end_time = part_t_abs + int(part.playTime)
                    if t_abs < part_t_abs or t_abs > part_end_time:
                        continue # t 不在这个 part 内，跳过整个 part
                    t_in_part = t_abs - part_t_abs
                part_result = part.search_vcc(t=t_in_part, ID=ID, value=value)
                yield part_result 

        return list(itertools.chain.from_iterable(_get_vccs_from_parts()))

    def get_vnote_from_time_range(self, start_time: Union[str, int, None]=None, end_time: Union[str, int, None]=None) -> List[VCC]:
        """获取指定时间范围内的音符列表"""
        if start_time is not None:
            VNOTE.check_int(value=start_time,name='start_time',minv=0)
            start_time = int(start_time)
        if end_time is not None:
            VNOTE.check_int(value=end_time,name='end_time',minv=0)
            end_time = int(end_time)
        
        def _get_notes_from_parts() -> Iterator[List[VNOTE]]:
            for part in self.vsPart:
                part_start_time = int(part.t)
                part_end_time = part_start_time + int(part.playTime)
                if part_end_time < (start_time if start_time is not None else 0) or part_start_time > (end_time if end_time is not None else float('inf')):
                    continue
                part_result = part.get_vnote_from_time_range(
                    start_time=(start_time - part_start_time) if start_time is not None else None,
                    end_time=(end_time - part_start_time) if end_time is not None else None
                )
                yield part_result
        return list(itertools.chain.from_iterable(_get_notes_from_parts()))
    
    def get_vcc_from_time_range(self, start_time: Union[str, int, None]=None, end_time: Union[str, int, None]=None) -> List[VCC]:
        """获取指定时间范围内的VCC点列表"""
        if start_time is not None:
            VCC.check_int(value=start_time,name='start_time',minv=0)
            start_time = int(start_time)
        if end_time is not None:
            VCC.check_int(value=end_time,name='end_time',minv=0)
            end_time = int(end_time)
        
        def _get_vccs_from_parts() -> Iterator[List[VCC]]:
            for part in self.vsPart:
                part_start_time = int(part.t)
                part_end_time = part_start_time + int(part.playTime)
                if part_end_time < (start_time if start_time is not None else 0) or part_start_time > (end_time if end_time is not None else float('inf')):
                    continue
                part_result = part.get_vcc_from_time_range(
                    start_time=(start_time - part_start_time) if start_time is not None else None,
                    end_time=(end_time - part_start_time) if end_time is not None else None
                )
                yield part_result
        return list(itertools.chain.from_iterable(_get_vccs_from_parts()))

    def delete_note(self, vnote: VNOTE) -> None:
        """删除指定的音符实例"""
        for part in self.vsPart:
            try:
                part.delete_vnote(vnote)
                return
            except ValueError:
                continue
        raise ValueError("The specified VNOTE instance is not found in any vsPart.")

    def delete_cc(self, vcc: VCC) -> None:
        """删除指定的VCC实例"""
        for part in self.vsPart:
            try:
                part.delete_vcc(vcc)
                return
            except ValueError:
                continue
        raise ValueError("The specified VCC instance is not found in any vsPart.")

    def cover_period_note(self, new_vnotes: List[VNOTE]) -> None:
        """用新的音符列表覆盖指定时间段内的音符.**注意**: new_vnotes中的音符的t均为绝对时间。"""
        sorted_new_vnotes = sorted(new_vnotes)
        if len(sorted_new_vnotes) == 0:
            return
        start_time = int(sorted_new_vnotes[0].t)
        end_time = int(sorted_new_vnotes[-1].t) + int(sorted_new_vnotes[-1].dur)

        for part in self.vsPart:
            part_start_time = int(part.t)
            part_end_time = part_start_time + int(part.playTime)
            if part_end_time < start_time or part_start_time > end_time:
                continue
            part_new_vnotes = [
                note for note in sorted_new_vnotes
                if int(note.t) + int(note.dur) > part_start_time and int(note.t) < part_end_time
            ]
            for note in part_new_vnotes:
                note.t = str(int(note.t) - part_start_time)
            part.cover_period_vnote(part_new_vnotes)

    def cover_period_cc(self, new_vccs: List[VCC]) -> None:
        """用新的VCC列表覆盖指定时间段内的VCC点.**注意**: new_vccs中的VCC点的t均为绝对时间。"""
        sorted_new_vccs = sorted(new_vccs)
        if len(sorted_new_vccs) == 0:
            return
        start_time = int(sorted_new_vccs[0].t)
        end_time = int(sorted_new_vccs[-1].t)

        for part in self.vsPart:
            part_start_time = int(part.t)
            part_end_time = part_start_time + int(part.playTime)
            if part_end_time < start_time or part_start_time > end_time:
                continue
            part_new_vccs = [
                vcc for vcc in sorted_new_vccs
                if int(vcc.t) > part_start_time and int(vcc.t) < part_end_time
            ]
            for vcc in part_new_vccs:
                vcc.t = str(int(vcc.t) - part_start_time)
            part.cover_period_vcc(part_new_vccs)
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
