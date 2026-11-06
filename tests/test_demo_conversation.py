from __future__ import annotations

import unittest

from agent import AgentRuntime


class DemoConversationTests(unittest.TestCase):
    movie = {
        "id": "coco-2017",
        "title_zh": "寻梦环游记",
        "themes": ["家庭", "梦想"],
    }

    def reply(self, message: str, history: list[dict[str, str]] | None = None) -> str:
        return AgentRuntime._demo_response(
            "discussion",
            message,
            self.movie,
            True,
            [],
            history=history,
        )

    def test_different_messages_do_not_receive_one_fixed_reply(self) -> None:
        liked = self.reply("我很喜欢爸爸最后的选择")
        confused = self.reply("为什么米格一定要离开家？")

        self.assertNotEqual(liked, confused)
        self.assertIn("爸爸最后的选择", liked)
        self.assertIn("为什么米格一定要离开家", confused)

    def test_repeated_message_avoids_repeating_recent_assistant_reply(self) -> None:
        first = self.reply("我觉得结尾有点难受")
        second = self.reply(
            "我觉得结尾有点难受",
            [
                {"role": "user", "content": "我觉得结尾有点难受"},
                {"role": "assistant", "content": first},
            ],
        )

        self.assertNotEqual(first, second)

    def test_general_follow_up_uses_previous_user_context(self) -> None:
        reply = self.reply(
            "我还是放不下那个选择",
            [{"role": "user", "content": "我觉得他其实很孤独"}],
        )

        self.assertIn("我觉得他其实很孤独", reply)


if __name__ == "__main__":
    unittest.main()
