from peewee import *

database = MySQLDatabase(
    'HelloWorld', **{'charset': 'utf8',
                     'sql_mode': 'PIPES_AS_CONCAT',
                     'use_unicode': True,
                     'host': '1.116.231.146',
                     'port': 3306,
                     'user': 'helloworld',
                     'password': '!Q@W#E$R%T^Y&U*I(O0p'
                     }
)



class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class LuckyAreas(BaseModel):
    adcode = CharField(null=True)
    area_name = CharField(null=True)
    center = UnknownField(null=True)  # json
    lat = DecimalField(null=True)
    level = CharField(null=True)
    lng = DecimalField(null=True)
    parent_code = CharField(null=True)

    class Meta:
        table_name = 'lucky_areas'


class BilibiliUser(BaseModel):
    id = BigAutoField(primary_key=True)
    nickname = CharField(max_length=255, null=True, collation='utf8mb4_general_ci')
    mid = CharField(max_length=255, null=True, collation='utf8mb4_general_ci')
    sex = CharField(max_length=255, null=True, collation='utf8mb4_general_ci')
    face = CharField(max_length=255, null=True, collation='utf8mb4_general_ci')
    fans = BigIntegerField(null=True)
    friend = BigIntegerField(null=True)
    attention = BigIntegerField(null=True)
    likes = BigIntegerField(null=True)
    video = BigIntegerField(null=True)
    archive = BigIntegerField(null=True)

    class Meta:
        table_name = 'bilibili_user'


class Proverb(BaseModel):
    id = AutoField()
    left = CharField(max_length=255, null=True, collation='utf8mb4_bin')
    right = CharField(max_length=255, null=True, collation='utf8mb4_bin')
    type = IntegerField(null=True)
    class Meta:
        table_name = 'proverb'

if __name__ == '__main__':

    area = LuckyAreas.select().dicts
    print(area)