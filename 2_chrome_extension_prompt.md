
场景：客服系统自动对话插件，客服通过内部网站处理回复用户反馈的问题。

写一个 Chrome 智能对话插件， 用来读取页面上的最后一个展示用的文本标签，取出内容，自动调用服务端对话 API ， 获取到回复内容后，粘贴到页面的文本输入框中。

1.只要页面打开的时候，插件自动运行 2.要监听的网址可以配置 3.服务端的 API 是兼容 OpenAI 的 API（这个可以 mock，或者使用开源的项目搭建一个假的） 4.调用的对话 API 的服务端地址可以配置， 同时可以配置调用服务端要用到的 api key

触发时机：当客服打开内部网站， 从网站上收到用户反馈的问题时 （用户反馈的问题在页面上有展示，提取的方式可以配置）。 逻辑处理： 插件检测到用户反馈的问题文本时，拿最后的文本作为输入，调用远程 api 来对话。 粘贴到页面的文本框中。

插件里面可以配置的项有这几个： 1.自动监听的网页地址或者域名。 2.获取用户发送的消息（最后一条消息）的匹配规则（正则或者 CSS Selector 之类） 3.页面输入框的规则配置 （自动检测 input 框，或者配置一个规则） 4.服务端的地址， API Key


Nous-Hermes-2-Yi-34B, Nous-Capybara-7B-V1p9:
给出了 JavaScript 代码和 manifest 配置。

deepseek-coder-33b-instruct:
给出了 JavaScript 代码和 manifest 配置。

Snorkel-Mistral-PairRM-DPO, Nous-Hermes-2-Mixtral-8x7B-DPO:
给出了完整步骤。经过二次提示，给出了配置和 JavaScript 代码。

GPT-4 turbo:
给出了完整步骤，manifest 配置，JavaScript 代码，以及 HTML 代码。
