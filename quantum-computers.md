# 为什么你不需要了解量子计算机

前段时间刚看到诸如：如果量子计算机出来了，那是不是没有GPU什么事了之类的提问。感觉又是一个毫无依据的闪念。过了几天之后看到格雷格·伊根的推上转发了这样一篇arXiv上的论文，标题是：What You Shouldn't Know About Quantum Computers。直接翻译过来就是为什么你不需要了解量子计算机。

早先在微软总裁纳德拉的书《刷新》我们读到过未来的三大变革分别是：混合现实、人工智能和量子计算。那为什么现在这位作者Chris Ferrie会跳出来说你不需要了解呢？论文标题一下子就抓住了我的注意力，也趁此机会尝试用AI辅助阅读可以进行到何种地步。

先将用到的工具列出来：
- Perplexity + GPT4o
- Kimi
- Obsidian
- Obsidian Copilot（插件）
- 沉浸式阅读（浏览器插件）

****

在翻译Foreword的时候发现，前面将pdf丢给kimi然后让它全文翻译的效果是非常糟糕的，除了大量不知所云之外，还有翻译错误以及漏翻译几句的问题。因此想要企图通过kimi直接给出全文译文是不太现实的。还有一些比较口语化的表达，沉浸式翻译或者是kimi都做得不好，比如：

> 原文：Sorry, no, that's too good to be true
> +++++
> Kimi：对不起，不是的，那太好了，不可能是真的
> +++++
> 沉浸OpenAI翻译：抱歉，不是的，那太美好了，不可能
> +++++
> 最终我的翻译：很遗憾，这似乎有点过于理想化

另外还有一些句子字面上的意思很难翻译，通常可能还有稍微扩充下，比如：

> 原文：There's one amplitude for each thing you could possibly find the system doing when you look.
> +++++
> Kimi：有一个幅度对应于你查看系统时可能发现它在做的每一件事。
> +++++
> 沉浸OpenAI翻译：当你观察时，每个可能找到系统在做的事情都有一个振幅。
> +++++
> 最终需添加译注：对于系统在任何可能状态下的行为，都存在一个幅度。这意味着，无论你观察到什么，系统中的动作总是具有某种强度或程度。例如，当你观察到一张 JPEG 图像时，它的亮暗程度就是该图像在整个色彩空间内所占据的位置和强度。同样地，当你听到一首 FLAC 音乐时，它的音量也是该音乐在整个声音范围内所占据的位置和强度。这些幅度反映了系统（即图像或音频）中信息流动方式以及其相关属性（如色彩深浅、声音高低等）。因此，通过分析这些幅值来理解系统行为非常重要。

****

## 作者 Chris Ferrie

[克里斯·费里 - 维基百科 --- Chris Ferrie - Wikipedia](https://en.wikipedia.org/wiki/Chris_Ferrie)

这是一个有趣作者，且看本文推荐他的几本书的书名：

- Great Quotes from Great Scientists: Quotes, Lessons, and Universal Truths from the World's Greatest Scientific Minds
伟大科学家的伟大语录：来自世界最伟大科学思想家的语录、教训和普世真理

- Quantum Bullsh*t: How to Ruin Your Life With Advice From Quantum Physics
量子胡说八道：如何用量子物理的建议毁掉你的生活

- 42 Reasons To Hate The Universe (And One Reason Not To)
讨厌宇宙的 42 个理由（以及一个不讨厌的理由）

- Where Did The Universe Come From? And Other Cosmic Questions
宇宙是从哪里来的？以及其他宇宙问题

这些书名都蛮有意思，看起来有点幽默又有点较真。

翻开Chris的维基百科，你可以看到他有一整个系列的写给孩子的科普书籍，比如《Quantum Physics for Babies》（给婴儿的量子物理学）。同时他也是一位加拿大物理学家、数学家、研究员，一直在悉尼科技大学工程量子系统中心担任高级讲师。