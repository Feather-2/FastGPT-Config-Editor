import streamlit as st
import json
import os
import pandas as pd


# 初始化模型数据
if 'models.json' not in os.listdir():
    with open('models.json', 'w') as f:
        json.dump({"llmModels": []}, f)

def initialize_json_file():
    if not os.path.exists('models.json'):
        with open('models.json', 'w') as f:
            json.dump({"llmModels": []}, f, indent=4)

initialize_json_file()

def load_models():
    try:
        with open('models.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data["llmModels"]
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return []

def save_models(models):
    with open('models.json', 'w') as f:
        json.dump({"llmModels": models}, f, indent=4)  # 使用4个空格进行缩进

def add_or_update_model(model):
    models = load_models()
    model_names = [m['name'] for m in models]
    if model['name'] in model_names:
        # 更新现有模型
        index = model_names.index(model['name'])
        models[index] = model
    else:
        # 添加新模型
        models.append(model)
    save_models(models)

def delete_model(model_name):
    models = load_models()
    models = [m for m in models if m['name'] != model_name]
    save_models(models)

def move_model_up(index):
    models = load_models()
    if index > 0:
        models[index], models[index - 1] = models[index - 1], models[index]
        save_models(models)

def move_model_down(index):
    models = load_models()
    if index < len(models) - 1:
        models[index], models[index + 1] = models[index + 1], models[index]
        save_models(models)

def edit_model_dialog(model):
    with st.form(key=f"form_{model['name']}"):
        model['model'] = st.text_input("模型名称", value=model['model'])
        model['name'] = st.text_input("模型别名", value=model['name'])
        model['avatar'] = st.text_input("模型Logo URL", value=model['avatar'])
        model['maxContext'] = st.number_input("最大上下文", value=model['maxContext'])
        model['maxResponse'] = st.number_input("最大回复", value=model['maxResponse'])
        model['quoteMaxToken'] = st.number_input("最大引用内容", value=model['quoteMaxToken'])
        model['maxTemperature'] = st.number_input("最大温度", value=model['maxTemperature'])
        model['charsPointsPrice'] = st.number_input("积分/1k token", value=model['charsPointsPrice'])
        model['censor'] = st.checkbox("开启敏感校验", value=model['censor'])
        model['vision'] = st.checkbox("支持图片输入", value=model['vision'])
        model['datasetProcess'] = st.checkbox("设置为知识库处理模型", value=model['datasetProcess'])
        model['usedInClassify'] = st.checkbox("用于问题分类", value=model['usedInClassify'])
        model['usedInExtractFields'] = st.checkbox("用于内容提取", value=model['usedInExtractFields'])
        model['usedInToolCall'] = st.checkbox("用于工具调用", value=model['usedInToolCall'])
        model['usedInQueryExtension'] = st.checkbox("用于问题优化", value=model['usedInQueryExtension'])
        model['toolChoice'] = st.checkbox("支持工具选择", value=model['toolChoice'])
        model['functionCall'] = st.checkbox("支持函数调用", value=model['functionCall'])
        model['customCQPrompt'] = st.text_input("自定义文本分类提示词", value=model['customCQPrompt'])
        model['customExtractPrompt'] = st.text_input("自定义内容提取提示词", value=model['customExtractPrompt'])
        model['defaultSystemChatPrompt'] = st.text_input("对话默认携带的系统提示词", value=model['defaultSystemChatPrompt'])

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("保存修改"):
                add_or_update_model(model)
                st.success("模型更新成功！")
                st.experimental_rerun()
        with col2:
            if st.form_submit_button("删除模型"):
                delete_model(model['name'])
                st.success("模型删除成功！")
                st.experimental_rerun()

@st.experimental_dialog("编辑模型")
def show_edit_dialog(model):
    edit_model_dialog(model)

def confirm_delete_dialog(model_name):
    with st.form(key=f"confirm_delete_{model_name}"):
        st.write("确定要删除这个模型吗？")
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("确定"):
                delete_model(model_name)
                st.success("模型删除成功！")
                st.experimental_rerun()
        with col2:
            if st.form_submit_button("取消"):
                st.experimental_rerun()

@st.experimental_dialog("确认删除")
def show_confirm_delete_dialog(model_name):
    confirm_delete_dialog(model_name)

def main():
    st.title("config.json 模型管理器")

    # 读取模型数据
    models = load_models()

    # 显示模型数据
    if models:
        st.caption("基于One-API与FastGPT项目的config.json的管理器")
        st.markdown("---")
        for i, model in enumerate(models):
            with st.expander(model['name']):
                col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
                with col1:
                    if st.button("上移", key=f"move_up_{i}"):
                        move_model_up(i)
                        st.experimental_rerun()
                with col2:
                    if st.button("下移", key=f"move_down_{i}"):
                        move_model_down(i)
                        st.experimental_rerun()
                with col3:
                    if st.button("修改", key=f"edit_{i}"):
                        show_edit_dialog(model)
                with col4:
                    if st.button("删除", key=f"delete_{i}"):
                        show_confirm_delete_dialog(model['name'])
                # 创建表格数据
                table_data = {
                    "属性": [
                        "模型名称", "模型别名", "模型Logo URL", "最大上下文", "最大回复", "最大引用内容", "最大温度", "积分/1k token",
                        "开启敏感校验", "支持图片输入", "设置为知识库处理模型", "用于问题分类", "用于内容提取", "用于工具调用", "用于问题优化",
                        "支持工具选择", "支持函数调用", "自定义文本分类提示词", "自定义内容提取提示词", "对话默认携带的系统提示词"
                    ],
                    "值": [
                        model['model'], model['name'], model['avatar'], model['maxContext'], model['maxResponse'], model['quoteMaxToken'],
                        model['maxTemperature'], model['charsPointsPrice'], model['censor'], model['vision'], model['datasetProcess'],
                        model['usedInClassify'], model['usedInExtractFields'], model['usedInToolCall'], model['usedInQueryExtension'],
                        model['toolChoice'], model['functionCall'], model['customCQPrompt'], model['customExtractPrompt'],
                        model['defaultSystemChatPrompt']
                    ]
                }

                # 转换为 DataFrame
                df = pd.DataFrame(table_data)

                # 计算每列的行数
                num_rows = len(df)
                rows_per_col = (num_rows + 1) // 2  # 向上取整


                # 分割数据到三列
                col1_data = df.iloc[:rows_per_col]
                col2_data = df.iloc[rows_per_col:]


                # 创建三列
                col1, col2 = st.columns(2)

                # 在每列中显示表格
                with col1:
                    st.table(col1_data)
                with col2:
                    st.table(col2_data)

    else:
        st.info("没有可用的模型。请添加一个新模型。")

    # 添加或更新模型
    with st.sidebar:
        st.subheader("添加或更新模型")
        new_model = {}

        col11, col12 = st.columns(2)
        with col11:

            # 模型名(对应OneAPI中渠道的模型名)
            new_model['model'] = st.text_input("模型名称", value="gpt-3.5-turbo", key="new_model_model")

            # 模型别名
            new_model['name'] = st.text_input("模型别名", value="gpt-3.5-turbo", key="new_model_name")

            # 模型的logo
            avatar_options = [
                "baichuan.svg",
                "chatglm.svg",
                "claude.svg",
                "deepseek.svg",
                "ernie.svg",
                "gemini.svg",
                "groq.svg",
                "huggingface.svg",
                "meta.svg",
                "minimax.svg",
                "moonshot.svg",
                "openai.svg",
                "qwen.svg",
                "sparkDesk.svg",
                "step.svg",
                "yi.svg"
            ]
            new_model['avatar'] = st.selectbox("模型Logo URL", options=avatar_options, index=avatar_options.index("openai.svg"), key="new_model_avatar")
            # n积分/1k token（商业版）
            new_model['charsPointsPrice'] = st.number_input("积分/1k token", value=0, key="new_model_charsPointsPrice")

        with col12:
            new_model['avatar'] = f"/imgs/model/{new_model['avatar']}"

            # 最大上下文
            new_model['maxContext'] = st.number_input("最大上下文", value=16000, key="new_model_maxContext")

            # 最大回复
            new_model['maxResponse'] = st.number_input("最大回复", value=4000, key="new_model_maxResponse")

            # 最大引用内容
            new_model['quoteMaxToken'] = st.number_input("最大引用内容", value=13000, key="new_model_quoteMaxToken")

            # 最大温度
            new_model['maxTemperature'] = st.number_input("最大温度", value=1.2, key="new_model_maxTemperature")
        
        col22,col23,col24 = st.columns(3)
        with col22:

            # 是否开启敏感校验（商业版）
            new_model['censor'] = st.checkbox("开启敏感校验", value=False, key="new_model_censor")

            # 是否支持图片输入
            new_model['vision'] = st.checkbox("支持图片输入", value=False, key="new_model_vision")


            # 是否支持函数调用（分类，内容提取，工具调用会用到。会优先使用 toolChoice，如果为false，则使用 functionCall，如果仍为 false，则使用提示词模式）
            new_model['functionCall'] = st.checkbox("支持函数调用", value=False, key="new_model_functionCall")

        with col23:
            # 是否设置为知识库处理模型（QA），务必保证至少有一个为true，否则知识库会报错
            new_model['datasetProcess'] = st.checkbox("知识库处理模型", value=True, key="new_model_datasetProcess")

            # 是否用于问题分类（务必保证至少有一个为true）
            new_model['usedInClassify'] = st.checkbox("用于问题分类", value=True, key="new_model_usedInClassify")
            # 是否支持工具选择（分类，内容提取，工具调用会用到。目前只有gpt支持）
            new_model['toolChoice'] = st.checkbox("支持工具选择", value=True, key="new_model_toolChoice")

        with col24:
            # 是否用于内容提取（务必保证至少有一个为true）
            new_model['usedInExtractFields'] = st.checkbox("用于内容提取", value=True, key="new_model_usedInExtractFields")

            # 是否用于工具调用（务必保证至少有一个为true）
            new_model['usedInToolCall'] = st.checkbox("用于工具调用", value=True, key="new_model_usedInToolCall")

            # 是否用于问题优化（务必保证至少有一个为true）
            new_model['usedInQueryExtension'] = st.checkbox("用于问题优化", value=True, key="new_model_usedInQueryExtension")
        col32,col33 = st.columns(2, vertical_alignment="bottom")
        with col32:
            # 自定义文本分类提示词（不支持工具和函数调用的模型）
            new_model['customCQPrompt'] = st.text_input("自定义文本分类提示词", key="new_model_customCQPrompt")

            # 自定义内容提取提示词
            new_model['customExtractPrompt'] = st.text_input("自定义内容提取提示词", key="new_model_customExtractPrompt")
        with col33:
            # 对话默认携带的系统提示词
            new_model['defaultSystemChatPrompt'] = st.text_input("对话默认携带的系统提示词", key="new_model_defaultSystemChatPrompt")

            # 请求API时，挟带一些默认配置（比如 GLM4 的 top_p）
            new_model['defaultConfig'] = {}

            update_model =  st.button("添加或更新模型", key="add_or_update_model")
            
        if update_model:
            add_or_update_model(new_model)
            st.success("模型添加或更新成功！")
            st.experimental_rerun()

if __name__ == "__main__":
    main()
