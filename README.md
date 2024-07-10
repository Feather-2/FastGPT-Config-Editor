# FastGPT-Config-Editor

## 简介

这是一个基于 Streamlit 的图形界面工具，用于管理 FastGPT 项目中的 `config.json` 文件中的模型配置。

## 功能

- 查看现有模型及其配置
- 添加新模型
- 更新现有模型配置
- 删除模型
- 上移/下移模型顺序

## 使用方法

1. 确保已安装 Python, Streamlit(≥1.36.0)与pandas。
2. 克隆此仓库或下载代码。
3. 在终端中运行 `streamlit run app.py`。
4. 在浏览器中访问 `http://localhost:8501` 。

## 配置说明

### 模型属性

| 属性 | 说明 |
|---|---|
| `model` | 模型名称（对应 OneAPI 中渠道的模型名） |
| `name` | 模型别名 |
| `avatar` | 模型 Logo URL |
| `maxContext` | 最大上下文 |
| `maxResponse` | 最大回复 |
| `quoteMaxToken` | 最大引用内容 |
| `maxTemperature` | 最大温度 |
| `charsPointsPrice` | 积分/1k token（商业版） |
| `censor` | 是否开启敏感校验（商业版） |
| `vision` | 是否支持图片输入 |
| `datasetProcess` | 是否设置为知识库处理模型（QA） |
| `usedInClassify` | 是否用于问题分类 |
| `usedInExtractFields` | 是否用于内容提取 |
| `usedInToolCall` | 是否用于工具调用 |
| `usedInQueryExtension` | 是否用于问题优化 |
| `toolChoice` | 是否支持工具选择 |
| `functionCall` | 是否支持函数调用 |
| `customCQPrompt` | 自定义文本分类提示词 |
| `customExtractPrompt` | 自定义内容提取提示词 |
| `defaultSystemChatPrompt` | 对话默认携带的系统提示词 |
| `defaultConfig` | 请求 API 时，挟带一些默认配置（比如 GLM4 的 top_p） |

## 注意事项

- 确保 `models.json` 文件存在于与 `app.py` 相同的目录下。
- 至少有一个模型的 `datasetProcess`、`usedInClassify`、`usedInExtractFields`、`usedInToolCall` 和 `usedInQueryExtension` 属性设置为 `True`。
- 只管理"llmModels"这部分
