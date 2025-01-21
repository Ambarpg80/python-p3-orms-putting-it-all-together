import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:

    def __init__(self, name, breed, id=None): #instatiates object instances
        self.id = id
        self.name= name
        self.breed = breed

    @classmethod                         #Creates table
    def create_table(cls):
        sql = """CREATE TABLE IF NOT EXISTS dogs(
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )"""
        CURSOR.execute(sql)

    @classmethod                         #Drops table
    def drop_table(cls):
        sql = """DROP TABLE IF EXISTS dogs"""
        CURSOR.execute(sql)

    def save(self): #adds id or inserts dog to DB
        dog = Dog(self.name, self.breed)                 
        sql = """INSERT INTO dogs (name,breed)       
            VALUES (?,?)"""
        if dog.id == None:
            added_dog = CURSOR.execute(sql,(self.name, self.breed))
            self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
        return added_dog
        


    @classmethod                        #instantiaties dog and inserts it to DB
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    

    @classmethod
    def new_from_db(cls, row):          #returns dog object from DB. A row is a tuple
        dog = cls(
            name = row[1], 
            breed = row[2],
            id = row[0])
        return dog 
    
    @classmethod                        #returns list of all dog objects from DB
    def get_all(cls):
        sql= """ SELECT * FROM dogs"""
        all_dogs = CURSOR.execute(sql).fetchall()
        dog_list = [cls.new_from_db(dog) for dog in all_dogs]
        return dog_list
    
    @classmethod
    def find_by_name(cls,name):
        sql = """ SELECT * FROM dogs
              WHERE name = ?
              LIMIT 1"""
        dog = CURSOR.execute(sql, (name, )).fetchone()
        if not dog:  # return None if no row/dog is found
            return None
        return cls.new_from_db(dog)
        
    

    @classmethod
    def find_by_id(cls,id):
        sql = """ SELECT * FROM dogs
              WHERE id = ?
              LIMIT 1"""
        dog = CURSOR.execute(sql,(id,)).fetchone()
        if not dog:  # return None if no row/dog is found
            return None
        return cls.new_from_db(dog)
    
    @classmethod
    def find_or_create_by(cls, name , breed):
        sql = """SELECT * FROM dogs
              WHERE name = ? AND breed = ?
              LIMIT 1"""
        dog = CURSOR.execute(sql,(name,breed)).fetchone()
        if dog:
            return cls.new_from_db(dog) 
        else: 
            new_dog = Dog(name, breed)
            new_dog.save()
            return new_dog


    def update(self):
        sql = """UPDATE dogs
              SET name = ? , breed = ?
              WHERE id =? """
        updated_dog = CURSOR.execute(sql,( self.name, self.breed, self.id,))
        return  updated_dog