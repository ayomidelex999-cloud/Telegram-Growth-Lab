from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from checker.analyzer import analyze_text, format_report

router = Router()

WELCOME = (
    "👋 <b>Ads & Prohibited Content Checker</b>\n\n"
    "Send me your ad copy or channel post text and I'll scan it for the "
    "policy issues that most commonly cause Telegram Ads rejections or "
    "content strikes (prohibited goods, misleading claims, spammy "
    "formatting, missing disclaimers, etc.).\n\n"
    "Commands:\n"
    "/check <text> — analyze specific text\n"
    "Or just send/forward a message and I'll check it directly.\n\n"
    "⚠️ This is a heuristic pre-check, not an official Telegram decision — "
    "it helps you catch and fix issues before you submit."
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(WELCOME)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(WELCOME)


@router.message(Command("check"))
async def cmd_check(message: Message):
    text = message.text.partition(" ")[2].strip()
    if not text and message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption or ""
    if not text:
        await message.answer(
            "Send the ad text after the command, e.g.:\n"
            "<code>/check Join now for guaranteed 200% profit!!!</code>\n"
            "or reply to a message with /check."
        )
        return
    report = analyze_text(text)
    await message.answer(format_report(report))


# Fallback: any plain text message (not a command) gets auto-checked.
@router.message(F.text & ~F.text.startswith("/"))
async def auto_check(message: Message):
    report = analyze_text(message.text)
    await message.answer(format_report(report))


# Also check captions on forwarded/media posts
@router.message(F.caption)
async def auto_check_caption(message: Message):
    report = analyze_text(message.caption)
    await message.answer(format_report(report))
