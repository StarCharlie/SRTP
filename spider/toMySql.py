import pandas as pd
import sqlalchemy

def toMySql():

    configure = {
        "DATABASE": "aijiu",
        "USER": "root",
        "PASSWORD": "syt20010907",
        "TABLE": "xuewei",
        "HOST": "localhost",
        "PORT": "3306",
        "CHARSET": "utf8",
        "EXCEL_PATH": r"C:\Users\HUAWEI\Desktop\aijiu.xlsx",
    }
    connect_sql = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset={5}".format(configure['USER'], configure['PASSWORD'],
                                                                           configure['HOST'], configure['PORT'],
                                                                           configure['DATABASE'], configure['CHARSET'],
                                                                           )
    engine = sqlalchemy.create_engine(connect_sql)
    df = pd.read_excel(configure['EXCEL_PATH'])
    df.to_sql(name='xuewei', con=engine, if_exists='replace', index=False)

    with engine.connect() as con:
        con.execute("""ALTER TABLE `{}`.`{}` \
                ADD COLUMN `id` INT NOT NULL AUTO_INCREMENT FIRST, \
                ADD PRIMARY KEY (`id`);"""
                    .format(configure['DATABASE'], configure['TABLE']))


if __name__ == "__main__":
    toMySql()
