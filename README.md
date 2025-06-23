# NyaaNBS

由于NBS开发组声明不官方支持而存在的DiscJockey/Notebot专用NBS曲库。这不是我的私人曲库，欢迎任何人加入。
A NBS library to support DiscJockey/Notebot, exist because NBS dev team decided not to. This is not private library, wellcome anyone joining.

![Using](./assets/JukeBox3.6v3-Using.png)

**Contributer**

暂时只有我自己...
Still only me...

## 目录 Catalog

- [快速开始 / QuickStart](#快速开始--quickstart)
- [游戏中使用 / Usage](#游戏中使用--usage)
- [排疑解难 / Trouble Shoot](#排疑解难--trouble-shoot)
- [贡献指南 / Contribution](#贡献指南--contribution)

## 快速开始 / QuickStart

1. **获取NBS文件 / GetNBS**

   If you have Git: **win+R, "cmd"**

   ```bash
   git clone https://github.com/Akitsuki4852/NyaaNBS.git
   ```

   或者点击右上角**绿色按钮**下载压缩包

   Or download zip via the **green button** in top righthand corner
2. **安装模组 / install:**

   DiscJockey: https://www.curseforge.com/minecraft/mc-mods/disc-jockey

   或 or

   任意挂端的 [Notebot](https://github.com/Victormeriqui/Notebot) </br>

   Use [Notebot](https://github.com/Victormeriqui/Notebot) function in ANY Hacked Client

   -> .minecraft/mods/
3. **DiscJockey**

   MerryChristmas.nbs </br>
   -> .minecraft/config/discjockey/songs/
4. **HackedClient**

   -> .minecraft/***client/notebot/
5. NBS (如果你想编曲 if you want to arrange yourself)

   https://noteblock.studio/

## 游戏中使用 / Usage

1. **DiscJockey**

   如果使用非原版交互距离音乐盒，在Mod Menu模组设定中找到”期望版本“，选择1.20.5+ </br>
   If using non-vanilla-reach MusicBox, find "expected version" in Mod Menu config, select 1.20.5+

   进入音乐盒明显标识的中心点，使用/DiscJockey 或 J键 (可更改)打开模组面板，选择前面提到的已经搬运进文件夹的.nbs文件，点击播放。</br>
   Stand inside the expected position in MusicBox, open DJ panel with /DiscJockey or J key (Changable), select your desired .nbs file, play and enjoy.
2. **Notebot**

   进入音乐盒明显标识的中心点，打开Notebot的选曲界面，选择前面提到的已经搬运进文件夹的.nbs文件，立即播放。</br>
   Stand inside the expected position in MusicBox, open notebot panel in your Client, select your desired .nbs file, play and enjoy.

## 舞台搭建指南 / Stage Buildup

![JukeBox3.6v4-1](./assets/JukeBox3.6v4-1.jpg)

核心原则：只要所有音符盒位于玩家交互范围内且不被遮挡。 </br>
Core Principle: Ensure every noteblock is reachable by player and is playable.

你可以使用MiniHud根据以下参数画球体划出范围： </br>
You can use MiniHud Mod to draw the range ball with following data:

- Player Camera Height: +1.6
- Vanilla Reach: 5.5

推荐将相同方块聚集摆放，且将南瓜/灵魂沙/萤石/浮冰堆放到较远离观众方向。</br>
It is recommanded to place same blocks together, while pumpkin/soulsand/glowstone/ice parts stay in the side away from audiences.

推荐使用提供的投影: </br>
Recommand using our provided schematics:

- vanilla reach : [Jukebox0.0v2](./schematics/Jukebox0.0v2.litematic)
- +1.2 reach : [Jukebox1.2v1](./schematics/Jukebox1.2v1.litematic)
- +3.6 reach : [Jukebox3.6v2](./schematics/Jukebox3.6v2.litematic)

## 排疑解难 / Trouble Shoot

一些你可能会遇到的问题: </br>
Some problem you might encounter:

- 缺少音色 Missing Timbre:

  - 请检查是否需要交互距离工具。请检查是否打开DJ mod 1.20.5+选项。如未发现问题请检查音乐盒投影。
  - Check if you need a tool for increasing your reach. Check if you had opened DJ mod 1.20.5+ config. If so please verify musicbox using provided schmetic.
- 游戏崩溃 Crash:

  - 不要使用DJ mod播放含有自定义乐器的.nbs。不要在空白曲库点击随机播放。
  - Do not use customized instrument with DJ mod. Do not click random play with empty music library.
- 听起来怪怪的 Sounds Weird?

  - 检查nbs内是否有超音域音符，右上角一键去除。
  - Check and remove out of range notes in your .nbs file, click top right corner in NBS.
- 发包超出限制踢出。 Kicked by sending package too freq.

  - 视乎服务器限制。建议换一份nbs。
  - Depends by server, just skip this nbs.
- 播放时音符盒不见了 Noteblock Disappearing?

  - 不要手持斧头进行播放。请立即停止并维修。
  - Do not use axe for playing. Stop and repair your musicbox.

## 参与指南 / Contribution

PR, Collab, or QQ1049026039。

暂无人参与，我也不知道应该是什么形式。

Still no one yet, I dont even know how it should started.

## 声明 Statement

### 资源中立性声明 / Neutrality Statement

本资源库仅作为音乐文件共享平台，不代表维护者支持或认可任何原创作者的政治倾向、立场及观点。使用者应对内容自行判断。

This repository serves solely as a music file sharing platform. It does not represent the maintainer's endorsement of any original authors' political tendencies, positions or viewpoints. Users shall exercise independent judgment regarding content appropriateness.

### 版权响应 / Copyright Compliance

所有文件版权归属原作者及权利人。收到版权方正式通知后，我们将在48小时内移除争议内容。侵权通知请提交至：akitsuki4852@gmail.com

All files belong to their respective copyright holders. Upon receiving formal notice from rights owners, we will remove disputed content within 24 hours. Submit DMCA requests to: akitsuki4852@gmail.com

### 无担保声明 / No Warranty

资源按"现状"提供，维护者不承诺：

- 音色与游戏版本的永久兼容性
- 文件完全无版权争议
- 资源存储的永久可用性

Resources provided "AS IS" with no warranties:

- Permanent compatibility with game versions
- Complete absence of copyright disputes
- Permanent availability of resources

### 使用者责任 / User Responsibility

使用者需确保：

- 遵守服务器插件政策（如禁止Notebot）
- 不将资源用于商业盈利

Users shall ensure:

- Compliance with server plugin policies (e.g. Notebot restrictions)
- Non-commercial usage

### 免责条款 / Limitation of Liability

维护者不对以下情况：

- 因使用资源导致的账号封禁
- 文件下载引发的系统安全问题

Maintainers not liable for:

- Account bans caused by resource usage
- System security issues from file downloads

### 协议变更权 / Terms Modification

我们保留随时更新本声明的权利，恕不另行通知。</br>
We reserve the right to modify these terms at any time without prior notice.
