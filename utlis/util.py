from peewee import fn

from settings.model import Proverb


def random_content():
    # proverb = Proverb.select().order_by(fn.Random()).get()
    proverb = Proverb.select().order_by(fn.Rand()).limit(1).get()
    proverb = f"{proverb.left}-----{proverb.right}"
    return proverb


