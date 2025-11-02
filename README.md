# VsqxT

Vocaloid Vsqx 文件的操作工具。

## 基本用法

```python
from vsqxt import read, VNOTE, VCC

# 读取VSQX文件
vsqx_file = read("filename.vsqx")  # 返回一个VSQX4类

# 写入VSQX文件
vsqx_file.write("output.vsqx")
```

## VSQX4 文件结构详解

### 1. VSQX4 主类
VSQX4是整个文件的顶层容器，包含以下属性：

- **VSQX4.vVoiceTable** - 包含该工程内所有使用过的歌手的信息
- **VSQX4.mixer** - 包含混音器信息
- **VSQX4.masterTrack** - 包含主轨信息，如节拍和曲速
- **VSQX4.vsTrack** - (列表) 包含各轨信息，其中包含如音符和参数
- **VSQX4.monoTrack** - 单声道伴奏信息
- **VSQX4.stTrack** - 双声道（立体声）伴奏信息
- **VSQX4.aux** - 辅助信息（通常是VST插件信息）

### 2. mixer 混音器类
mixer 类包含所有轨道的混音设置：

- **mixer.masterUnit** - 主轨混音器
- **mixer.monoUnit** - 单声轨混音器
- **mixer.stUnit** - 伴奏轨混音器
- **mixer.vsUnits** - (列表) 各个人声轨混音器

### 3. masterTrack 主轨类
masterTrack 包含整个项目的时间和节拍信息：

- **masterTrack.return_beat()** - 返回节拍。如果整首曲子没变节拍返回一个节拍字符串，如果变节拍返回列表
- **masterTrack.return_bpm()** - 返回曲速。如果整首曲子没变速返回一个曲速值，如果变速返回列表
- **masterTrack.timeSig** - 拍号信息列表
- **masterTrack.tempo** - 速度信息列表
- **masterTrack.resolution** - 分辨率（通常为480）
- **masterTrack.preMeasure** - 预备小节数

### 4. vsTrack 人声轨类
一个 vsTrack 包含多个 parts，是音符和参数的容器：

- **vsTrack.tNo** - 这条轨是第几条轨
- **vsTrack.name** - 轨道名称
- **vsTrack.comment** - 轨道注释
- **vsTrack.vsPart** - (列表) 包含的所有Part
- **vsTrack.return_all_note()** - 返回这条轨中包含的所有音符
- **vsTrack.return_all_cc()** - 返回这条轨中包含的所有参数

#### 4.1 vsPart 类
vsPart 是音符和控制参数的基本容器：

- **vsPart.t** - Part的起始时间（相对于项目开始）
- **vsPart.playTime** - Part的长度
- **vsPart.name** - Part名称
- **vsPart.comment** - Part注释
- **vsPart.VCC** - (列表) 该part中所有参数
- **vsPart.VNote** - (列表) 该part中所有音符

##### 4.1.1 VCC 控制参数类
VCC 表示控制曲线上的一个点：

- **VCC.t** - 参数的时间位置
- **VCC.ID** - 参数的类型（如 'D'=动态, 'B'=呼吸度等）
- **VCC.v** - 参数的值

参数类型说明：
- `D/DYN` - 动态 (0-127)
- `B/BRN` - 呼吸度 (0-127)
- `R/BRI` - 明亮度 (0-127)
- `C/CLE` - 清晰度 (0-127)
- `G/GEN` - 性别系数 (0-127)
- `T/POR` - 滑音时间 (0-127)
- `X/XSY` - Cross Synthesis (0-127)
- `W/GWL` - 嘶吼度 (0-127)
- `P/PIT` - 音高弯曲 (-8192-8191)
- `S/PBS` - 音高弯曲灵敏度 (0-24)

##### 4.1.2 VNOTE 音符类
VNOTE 表示一个音符：

- **VNOTE.t** - 音符的起始时间位置
- **VNOTE.dur** - 音符的长度
- **VNOTE.n** - 音高 (MIDI音符号, 0-127)
- **VNOTE.v** - VEL参数 (0-127)
- **VNOTE.y** - 输入的歌词
- **VNOTE.p** - 发音标记
- **VNOTE.nStyle** - 音符样式参数

###### 4.1.2.1 nStyle 音符样式类
nStyle 包含音符的详细参数：

- **nStyle.accent** - 重音 (0-127)
- **nStyle.bendDep** - 弯音深度 (0-127)
- **nStyle.bendLen** - 弯音长度 (0-127)
- **nStyle.decay** - 衰减 (0-127)
- **nStyle.fallPort** - 降音 (0-1)
- **nStyle.opening** - OPE参数 (0-127)
- **nStyle.risePort** - 升音 (0-1)
- **nStyle.vibLen** - 颤音长度 (0-127)
- **nStyle.vibType** - 颤音类型 (0-127)
- **nStyle.vibDep.return_param()** - 返回颤音振幅参数列表
- **nStyle.vibRate.return_param()** - 返回颤音频率参数列表

### 5. monoTrack 和 stTrack 伴奏轨类
这两个类都包含 wavPart 列表：

- **wavPart.t** - 伴奏起始时间位置
- **wavPart.playTime** - 伴奏播放时间
- **wavPart.name** - 名称
- **wavPart.comment** - 注释
- **wavPart.filePath** - 伴奏文件路径
- **wavPart.fs** - 采样率
- **wavPart.rs** - 位深度
- **wavPart.nCh** - 声道数

---

## 高级 API 文档

### 时间转换 API

#### masterTrack.beat_to_t()
将小节、拍子位置转换为绝对时间（tick）

```python
beat_to_t(bar: int, beat: int = 1, pos_in_bar: int = 0, pre_bar: bool = False) -> int
```

参数说明：
- `bar`: 小节号（从1开始）
- `beat`: 拍子号（从1开始）
- `pos_in_bar`: 拍内偏移（tick数）
- `pre_bar`: 是否包含预备小节，默认False

返回值：绝对时间位置（tick）

示例：
```python
# 获取第19小节第2拍第150tick的绝对时间
bar_t = vsqx_file.masterTrack.beat_to_t(bar=19, beat=2, pos=150)
print(f"绝对时间: {bar_t} ticks")
```

#### masterTrack.t_to_beat()
将绝对时间转换为小节、拍子位置

```python
t_to_beat(t: int, pre_bar: bool = False) -> Tuple[int, int, int]
```

参数说明：
- `t`: 绝对时间（tick）
- `pre_bar`: 是否包含预备小节，默认False

返回值：(小节号, 拍子号, 拍内偏移)

示例：
```python
# 将绝对时间7680转换为小节位置
bar, beat, pos = vsqx_file.masterTrack.t_to_beat(t=7680)
print(f"位置: 第{bar}小节第{beat}拍第{pos}tick")
```

#### masterTrack.time_to_t()
将真实时间（分:秒:毫秒）转换为绝对时间

```python
time_to_t(minute: int = 0, second: int = 0, millisecond: int = 0) -> int
```

参数说明：
- `minute`: 分钟数
- `second`: 秒数
- `millisecond`: 毫秒数

返回值：绝对时间（tick）

示例：
```python
# 获取1分23秒对应的绝对时间
bar_t = vsqx_file.masterTrack.time_to_t(minute=1, second=23)
print(f"1分23秒 = {bar_t} ticks")
```

#### masterTrack.t_to_time()
将绝对时间转换为真实时间

```python
t_to_time(t: int) -> Tuple[int, int, int]
```

参数说明：
- `t`: 绝对时间（tick）

返回值：(分钟, 秒, 毫秒)

示例：
```python
# 将绝对时间转换为真实时间
minute, second, millisecond = vsqx_file.masterTrack.t_to_time(bar_t)
print(f"时间: {minute}分{second}秒{millisecond}毫秒")
```

---

### Part 管理 API

#### vsTrack.create_vspart()
创建一个新的 vsPart

```python
create_vspart(t='0', playTime='1920', name='NewPart', 
              comment='New Musical Part', sPlugs=[], pStyles=[], 
              singers=[], ccs=[], notes=[], plane=0)
```

参数说明：
- `t`: Part开始时间（绝对时间）
- `playTime`: Part长度
- `name`: Part名称
- `comment`: Part注释
- `sPlugs`: 插件信息（可选，默认使用第一个Part的设置）
- `pStyles`: 风格参数（可选）
- `singers`: 歌手信息（可选）
- `ccs`: 初始控制参数列表
- `notes`: 初始音符列表
- `plane`: 平面参数

示例：
```python
# 在第10小节创建新Part
bar_t = vsqx_file.masterTrack.beat_to_t(bar=10, beat=1, pos=0)
vsqx_file.vsTrack[0].create_vspart(t=bar_t)
```

---

### 音符操作 API

#### vsTrack.insert_note()
向轨道插入音符（自动找到合适的Part）

```python
insert_note(vnote: Union[VNOTE, None] = None, t='0', dur='1920', 
            n='60', v='64', y='a', p='a', accent='50', bendDep='8', 
            bendLen='0', decay='50', fallPort='0', opening='127', 
            risePort='0', vibLen='0', vibType='0', vibDep=[], 
            vibRate=[], lock='')
```

参数说明：
- `vnote`: VNOTE实例（如果提供则忽略其他参数）
- `t`: 音符开始时间（绝对时间）
- `dur`: 持续时间
- `n`: 音高 (0-127)
- `v`: 音量 (0-127)
- `y`: 歌词
- `p`: 发音
- 其他参数：音符样式参数

示例：
```python
# 方式1：使用VNOTE实例
vnote = VNOTE.create(t=bar_t, dur=480, n=60, y='o', p='o')
vsqx_file.vsTrack[0].insert_note(vnote)

# 方式2：直接提供参数
vsqx_file.vsTrack[0].insert_note(t=bar_t, dur=480, n=60, y='o', p='o')
```

#### vsTrack.search_note()
搜索符合条件的音符

```python
search_note(t=None, dur=None, n=None, v=None, y=None, p=None, 
            accent=None, bendDep=None, bendLen=None, decay=None, 
            fallPort=None, opening=None, risePort=None, vibLen=None, 
            vibType=None, vibDep=None, vibRate=None) -> List[VNOTE]
```

参数说明：所有参数都是可选的，提供的参数将作为搜索条件

返回值：符合条件的音符列表

示例：
```python
# 搜索特定时间的音符
notes = vsqx_file.vsTrack[0].search_note(t=bar_t)

# 搜索所有歌词为'a'的音符
notes = vsqx_file.vsTrack[0].search_note(y='a')
```

#### vsTrack.get_vnote_from_time_range()
获取时间范围内的音符

```python
get_vnote_from_time_range(start_time=None, end_time=None) -> List[VNOTE]
```

参数说明：
- `start_time`: 开始时间（绝对时间）
- `end_time`: 结束时间（绝对时间）

返回值：时间范围内的音符列表

示例：
```python
# 获取第39小节第2拍到第40小节第1拍之间的音符
start = vsqx_file.masterTrack.beat_to_t(39, 2, 420)
end = vsqx_file.masterTrack.beat_to_t(40, 1, 450)
notes = vsqx_file.vsTrack[0].get_vnote_from_time_range(start, end)
```

#### vsTrack.delete_note()
删除指定音符

```python
delete_note(vnote: VNOTE) -> None
```

参数说明：
- `vnote`: 要删除的音符实例

示例：
```python
# 删除找到的第一个音符
notes = vsqx_file.vsTrack[0].search_note(t=bar_t)
if notes:
    vsqx_file.vsTrack[0].delete_note(notes[0])
```

#### vsTrack.cover_period_note()
用新音符列表覆盖指定时间段

```python
cover_period_note(new_vnotes: List[VNOTE]) -> None
```

参数说明：
- `new_vnotes`: 新音符列表（会根据时间范围自动覆盖）

示例：
```python
# 创建音阶
vnote_list = []
for i, y in enumerate(["a", "i", "u", "e", "o"]):
    vnote = VNOTE.create(t=bar_t + i*480, dur=480, n=60, y=y, p=y)
    vnote_list.append(vnote)
vsqx_file.vsTrack[0].cover_period_note(vnote_list)
```

---

### 控制参数操作 API

#### vsTrack.insert_cc()
向轨道插入控制参数

```python
insert_cc(vcc: Union[VCC, None] = None, typ='D', value='64', t='0')
```

参数说明：
- `vcc`: VCC实例（如果提供则忽略其他参数）
- `typ`: 参数类型 (如 'D', 'DYN' 等)
- `value`: 参数值
- `t`: 时间位置（绝对时间）

示例：
```python
# 方式1：使用VCC实例
vcc = VCC.create(t=bar_t, ID='DYN', v=120)
vsqx_file.vsTrack[0].insert_cc(vcc)

# 方式2：直接提供参数
vsqx_file.vsTrack[0].insert_cc(typ='DYN', value='120', t=str(bar_t))
```

#### vsTrack.search_cc()
搜索符合条件的控制参数

```python
search_cc(t=None, ID=None, value=None) -> List[VCC]
```

参数说明：
- `t`: 时间位置
- `ID`: 参数类型
- `value`: 参数值

返回值：符合条件的控制参数列表

示例：
```python
# 搜索特定时间的参数
vcc_list = vsqx_file.vsTrack[0].search_cc(t=bar_t)

# 搜索所有DYN参数
vcc_list = vsqx_file.vsTrack[0].search_cc(ID='D')
```

#### vsTrack.get_vcc_from_time_range()
获取时间范围内的控制参数

```python
get_vcc_from_time_range(start_time=None, end_time=None) -> List[VCC]
```

参数说明：
- `start_time`: 开始时间（绝对时间）
- `end_time`: 结束时间（绝对时间）

返回值：时间范围内的控制参数列表

示例：
```python
# 获取指定时间范围的参数
vcc_list = vsqx_file.vsTrack[0].get_vcc_from_time_range(start_time, end_time)
for vcc in vcc_list:
    if vcc.ID == "D":
        print(f"DYN value: {vcc.v}")
```

#### vsTrack.delete_cc()
删除指定控制参数

```python
delete_cc(vcc: VCC) -> None
```

参数说明：
- `vcc`: 要删除的控制参数实例

示例：
```python
# 删除时间范围内的所有参数
vcc_list = vsqx_file.vsTrack[0].get_vcc_from_time_range(start_time, end_time)
for vcc in vcc_list:
    vsqx_file.vsTrack[0].delete_cc(vcc)
```

#### vsTrack.cover_period_cc()
用新参数列表覆盖指定时间段

```python
cover_period_cc(new_vccs: List[VCC]) -> None
```

参数说明：
- `new_vccs`: 新控制参数列表

示例：
```python
# 创建正弦波形的音量控制
import numpy as np
A = 32  # 振幅
f = 1   # 频率
duration = 10
sampling_rate = 40
t = np.linspace(0, duration, int(duration * sampling_rate))
y_wave = A * np.sin(2 * np.pi * f * t) + 64

vcc_list = []
t_pos = bar_t
for y in y_wave:
    vcc = VCC.create(t=t_pos, ID='DYN', v=int(y))
    vcc_list.append(vcc)
    t_pos += 3

vsqx_file.vsTrack[0].cover_period_cc(vcc_list)
```

---

## 完整使用示例

```python
from vsqxt import read, VNOTE, VCC

# 读取文件
vsqx_file = read("test.vsqx")

# 时间转换示例
bar_t = vsqx_file.masterTrack.beat_to_t(bar=30, beat=2, pos=0)

# 创建并插入音符
vnote = VNOTE.create(t=bar_t, dur=480, n=60, y='o', p='o')
vsqx_file.vsTrack[0].insert_note(vnote)

# 创建并插入控制参数
vcc = VCC.create(t=bar_t, ID='DYN', v=120)
vsqx_file.vsTrack[0].insert_cc(vcc)

# 搜索和编辑
notes = vsqx_file.vsTrack[0].search_note(t=bar_t)
if notes:
    vsqx_file.vsTrack[0].delete_note(notes[0])

# 批量操作
vnote_list = []
for i, lyric in enumerate(['do', 're', 'mi', 'fa', 'so']):
    vnote = VNOTE.create(
        t=bar_t + i*480,
        dur=480,
        n=60 + i*2,
        y=lyric,
        p=lyric
    )
    vnote_list.append(vnote)
vsqx_file.vsTrack[0].cover_period_note(vnote_list)

# 保存文件
vsqx_file.write('result.vsqx')
```

---

## 更新历史

### 当前版本
- 完整的高级 API 支持
- 时间转换系统（小节/拍子/真实时间）
- 音符和参数的 CRUD 操作
- 批量编辑功能

### 0.0.2 (2021.10.1)
- 修复 name 或 comment 为空时读取出现 AttributeError 的 bug
- 修复 plugSR 不存在时读取失败的 bug
- 修复 VNote p 标签 lock 属性提取问题

## 已知问题

1. 写成 Vsqx 的时候每行前缩进会被省略（不影响 Vocaloid 读取文件）
2. read函数读取速度慢（TODO: 将列表append更改为列表表达式）

## 开发者

如需贡献代码或报告问题，请访问 [GitHub 仓库](https://github.com/mmkjj/VsqxT)
