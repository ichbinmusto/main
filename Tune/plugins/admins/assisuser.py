import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatJoinRequest
from Tune import app
from Tune.misc import SUDOERS
from Tune.utils.database import get_assistant
from Tune.utils.decorators import AdminRightsCheck

async def join_userbot(app, chat_id, chat_identifier=None) -> str:
    userbot = await get_assistant(chat_id)

    try:
        member = await app.get_chat_member(chat_id, userbot.id)
        if member.status == ChatMemberStatus.BANNED:
            await app.unban_chat_member(chat_id, userbot.id)
    except Exception as ex:
        logging.error(f"Error checking chat member status in chat {chat_id}: {ex}")

    try:
        if chat_identifier:
            await userbot.join_chat(chat_identifier)
        else:
            invite_link = await app.create_chat_invite_link(chat_id)
            await userbot.join_chat(invite_link.invite_link)
        return "**✅ Assistant joined.**"
    except Exception as join_exc:
        logging.error(f"Error during join_chat in chat {chat_id}: {join_exc}")
        try:
            if chat_identifier:
                await userbot.send_chat_join_request(chat_identifier)
            else:
                invite_link = await app.create_chat_invite_link(chat_id)
                await userbot.send_chat_join_request(invite_link.invite_link)
            return "**✅ Assistant sent a join request.**"
        except Exception as join_req_exc:
            logging.error(f"Error during send_chat_join_request in chat {chat_id}: {join_req_exc}")
            return f"Error: {str(join_req_exc)}"


@app.on_chat_join_request()
async def approve_join_request(client, chat_join_request: ChatJoinRequest):
    userbot = await get_assistant(chat_join_request.chat.id)
    if chat_join_request.from_user.id == userbot.id:
        await client.approve_chat_join_request(chat_join_request.chat.id, userbot.id)
        await client.send_message(
            chat_join_request.chat.id,
            "**✅ Assistant has been approved and joined the chat.**"
        )
    else:
        logging.info(
            f"Ignored join request from non-assistant user {chat_join_request.from_user.id} "
            f"in chat {chat_join_request.chat.id}"
        )


@app.on_message(
    filters.command(["userbotjoin", "assistantjoin"], prefixes=[".", "/"])
    & (filters.group | filters.private)
)
@AdminRightsCheck
async def join_group(app, message):
    chat_id = message.chat.id
    me = await app.get_me()
    status_message = await message.reply("**Please wait, inviting assistant...**")
    await asyncio.sleep(1)

    chat_member = await app.get_chat_member(chat_id, me.id)
    if chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        chat_identifier = message.chat.username
        response = await join_userbot(app, chat_id, chat_identifier=chat_identifier)
    else:
        response = "**I need admin power to invite my assistant.**"

    await status_message.edit_text(response)


@app.on_message(
    filters.command("userbotleave", prefixes=[".", "/"]) & filters.group
)
@AdminRightsCheck
async def leave_one(app, message):
    try:
        userbot = await get_assistant(message.chat.id)
        await userbot.leave_chat(message.chat.id)
        await app.send_message(
            message.chat.id, "**✅ Assistant successfully left this chat.**"
        )
    except Exception as ex:
        logging.error(f"Error during assistant leaving chat {message.chat.id}: {ex}")
        await message.reply(f"Error: {str(ex)}")


@app.on_message(filters.command(["leaveall"], prefixes=["."]) & SUDOERS)
async def leave_all(app, message):
    left = 0
    failed = 0
    status_message = await message.reply("🔄 **Assistant is leaving all chats!**")
    try:
        userbot = await get_assistant(message.chat.id)
        async for dialog in userbot.get_dialogs():

            if dialog.chat.id == -1002014167331:
                continue
            try:
                await userbot.leave_chat(dialog.chat.id)
                left += 1
                await status_message.edit_text(
                    f"**Assistant is leaving all chats...**\n\n**Left:** {left} chats.\n**Failed:** {failed} chats."
                )
            except Exception as exc:
                logging.error(f"Failed to leave chat {dialog.chat.id}: {exc}")
                failed += 1
                await status_message.edit_text(
                    f"**Assistant is leaving all chats...**\n\n**Left:** {left} chats.\n**Failed:** {failed} chats."
                )
            await asyncio.sleep(1)
    finally:
        await app.send_message(
            message.chat.id,
            f"**✅ Left from:** {left} chats.\n**❌ Failed in:** {failed} chats."
        )
