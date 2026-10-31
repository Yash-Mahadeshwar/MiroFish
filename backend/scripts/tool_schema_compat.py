"""
工具 schema 兼容补丁

CAMEL 为无参数的动作（如 do_nothing、trend）生成 `"properties": {}, "required": []`。
Groq 等严格校验的 OpenAI 兼容服务会拒绝这种 schema（400: 'required' present but
'properties' is missing），导致 Agent 每一轮的动作全部失败。
这里在 properties 为空时去掉 required 字段。
"""

from camel.toolkits import FunctionTool

_original_get_schema = FunctionTool.get_openai_tool_schema


def _get_schema_without_empty_required(self):
    schema = _original_get_schema(self)
    params = schema.get("function", {}).get("parameters")
    if isinstance(params, dict) and not params.get("properties"):
        params.pop("required", None)
    return schema


FunctionTool.get_openai_tool_schema = _get_schema_without_empty_required
