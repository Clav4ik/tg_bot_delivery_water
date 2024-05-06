from peewee import SqliteDatabase, Model, CharField, ForeignKeyField, BooleanField

db = SqliteDatabase('bot.sqlite3')
class User(Model):
    #object owner or manager
    user_tg_id = CharField(unique=True)

    class Meta:
        database = db

class Address(Model):
    object = CharField(null = True)
    name = CharField()
    street = CharField()
    house_num = CharField()
    office_num= CharField(null = True)

    user = ForeignKeyField(User)

    class Meta:
        database = db

class Phone_Number(Model):
    phone_number = CharField()
    user = ForeignKeyField(User)

    class Meta:
        database = db

class Black_List(Model):
    user_tg_id = CharField(unique=True, index=True)

    class Meta:
        database = db

class Token_Unblock(Model):
    token =CharField()
    used = BooleanField(default=False)

    class Meta:
        database = db

if __name__ == "__main__":
    db.create_tables([User, Address, Phone_Number, Black_List, Token_Unblock])