from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

from libraries.tool import hash
from libraries.maimaidx_music import *
from libraries.image import *
from libraries.maimai_best_40 import generate
from libraries.maimai_best_50 import generate50
import re


@register("基于mai-bot的Astrbot插件移植", "Boilingfish", "移植", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""



    async def song_txt(self,event:AstrMessageEvent,music: Music):
        chain = [
            Comp.At(qq = event.get_sender_id()),
            Comp.Plain(f"{music.id}. {music.title}\n"),
            Comp.Image.fromURL(f"https://www.diving-fish.com/covers/{get_cover_len5_id(music.id)}.png"),
            Comp.Plain(f"\n{'/'.join(music.level)}")
        ]
        yield event.chain_result(chain)
        
    async def inner_level_q(ds1, ds2=None):
        result_set = []
        diff_label = ['Bas', 'Adv', 'Exp', 'Mst', 'ReM']
        if ds2 is not None:
            music_data = total_list.filter(ds=(ds1, ds2))
        else:
            music_data = total_list.filter(ds=ds1)
        for music in sorted(music_data, key = lambda i: int(i['id'])):
            for i in music.diff:
                result_set.append((music['id'], music['title'], music['ds'][i], diff_label[i], music['level'][i]))
        return result_set
    @filter.command("b50")
    async def b50(self,event = AstrMessageEvent,username = str):
        if username == '':
            username = event.get_sender_id()
        else:
            event.Plain_result("目前仅支持查询自己的数据哦~")
        payload = {'qq': str(event.get_sender_id()),'b50':True}
        img, success = await generate50(payload)
        if success == 400:
            await event.Plain_result("未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。")
        elif success == 403:
            await event.Plain_result("该用户禁止了其他人获取数据。")
        else:
            chain = [
                Comp Image.fromURL(f"base64://{str(image_to_base64(img), encoding='utf-8')}")
            ]
            await event.chain_result(chain)



    
    
    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
