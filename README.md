# VsqxT

Vocaloid Vsqx 文件的操作工具。

## 基本指令

```python
import vsqx
VSQX4 = read(filename)  # 返回一个VSQX4类
```

```python
VSQX4.write(filename)  # 重新写成VSQX文件
```

## VSQX4类解析

> VSQX4的属性
> 1、VSQX4.vVoiceTables, 包含该工程内所有使用过的歌手的信息
> 2、VSQX4.mixers, 包含混响器信息
> 3、VSQX4.masterTracks,包含主轨信息，如节拍和曲速
> 4、VSQX4.vsTracks, （列表）包含各轨信息，其中包含如音符和参数
> 5、VSQX4.monoTracks, 单声道伴奏信息
> 6、VSQX4.stTracks,双声道伴奏信息
> 7、VSQX4.auxs，？应该是VST之类的吧，我没看懂


> 2 mixer类:
> mixer.masterUnit ,主轨混音器
> mixer.monoUnit，单声轨混音器
> mixer.stUnit，伴奏轨混音器
> mixer.vsUnits，（列表）各个人声轨混音器


> 3 masterTrack类：
> materTrack.returnBeat() 返回节拍。如果整首曲子没变节拍返回一个节拍字符串，如果变节拍返回列表
> materTrack.returnBPM() 返回曲速。如果整首曲子没变速返回一个曲速值，如果变速返回列表


>     4 vsTracks
>     一个vsTrack有多个parts
>     vsTracks.tNo 这条轨是第几条轨
>     vsTracks.return_all_note() 返回这条轨中包含的所有音符
>     vsTracks.rreturn_all_cc() 返回这条轨中包含的所有参数
>
>         4.1 vsTracks.vsPart (列表)
>         vsPart.t Part的起始时间
>         vsPart.playTime Part的长度
>         vsPart.VCC（列表） 该part中所有参数
>         vsPart.VNote（列表） 该part中所有音符
>
>             4.1.1 vsTracks.vsPart.VCC (列表)
>             VCC.t, 参数的时间位置
>             VCC.ID, 参数的类型
>             VCC.v 参数的值
>
>             4.1.2 vsTracks.vsPart.VNote（列表）
>             VNote.t 音符的起始时间位置
>                     VNote.dur 音符的长度
>                     VNote.n 音高
>                     VNote.v vel参数
>                     VNote.y 输入的歌词
>                     VNote.p 发音标记
>             VNote.nStyle 音符参数
>
>                 4.1.2.1 vsTracks.vsPart.VNote.nStyle
>                 nStyle.accent, 重音
>                 nStyle.bendDep, 弯音深度
>                 nStyle.bendLen, 弯音长度
>                 nStyle.decay, 衰减
>                 nStyle.fallPort, 降音
>                 nStyle.opening, OPE参数
>                 nStyle.risePort, 声音
>                 nStyle.vibLen, 颤音长度
>                 nStyle.vibType,颤音类型
>                 nStyle.vibDep.return_param()（返回列表）颤音振幅参数
>                 nStyle.vibRate.return_param() （返回列表）颤音频率参数


> 5、6 monoTracks、stTracks
> 都是包含一个列表，包括n个wavPart类
> monoTracks.wavPart.t 伴奏起始时间位置
> monoTracks.playTime 伴奏播放时间
> monoTracks.filePath 伴奏路径
> （stTracks同理）

## UpdateHistory

***2021.10.1 0.0.2***
修复name或comment为空时读取出现 AttributeError的bug 修复plugSR不存在时读取失败的bug

***********************
已知bug

1. VNote p标签有的时候会有<p lock="1">表示音符发声被保护，暂时没法提取出lock标签 (修复)
2. 写成Vsqx的时候每行前缩进会被省略（不影响vocaloid读取文件）

开发中的功能

1. vsTrack.create_vspart() 创建一个vspart
2. sorted(VCC)、sorted(VNote) 以各参数（音符）时间位置为基准进行排序
3. create_cc()create_note() 向某一轨创建一个参数（音符），并把它插入到合适的part、合适的位置中
4. getVCCbyID() 输入某一参数种类，返回vsPart或者vsTrack中全部该参数列表

*************************