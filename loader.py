import glob
import chordmodel
import chordparser
import redis
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filepath")
parser.add_argument("--host", default="localhost")

args= parser.parse_args()

r = redis.StrictRedis(host = args.host, port=6379, db=0)

file_list = glob.glob( args.filepath )

for file in file_list:
    ch = chordparser.get_universal( file )
    chordmodel.make_model( r, ch )
    print( file )
