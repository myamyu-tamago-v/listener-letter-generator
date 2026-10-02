import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class LLMConf(BaseModel):
    base_url: str = Field(
        description="LLM APIのBASE_URL",
    )
    model_name: str = Field(
        default="",
        description="使用するモデル銘",
    )
    api_key: str = Field(
        default="dummy_key",
        description="API Key。環境変数から取得する。",
    )


# LLMの設定
_conf: dict[str, LLMConf] = {
    "local_llama": LLMConf(
        base_url="http://localhost:18080",
    ),
    "gemini": LLMConf(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        model_name="gemini-3.5-flash-lite",
    ),
    "openrouter": LLMConf(
        base_url="https://openrouter.ai/api/v1",
        model_name="nvidia/nemotron-3-super-120b-a12b:free",  # gemmaが混んでて使えない
    ),
}


def get_llm_conf() -> LLMConf:
    """LLMの設定を取得"""
    key = os.environ.get("LLM_MODEL", "gemini")
    conf = _conf.get(key)
    if not conf:
        raise Exception("LLM設定が見つからない")
    conf.api_key = os.environ.get("LLM_API_KEY", "dummy_key")
    return conf
