from entities import *
import os

def create_save(save_id : str) -> None:
	os.mkdir(f"./saves/{save_id}", exist_ok = True)
	os.mkdir(f"./saves/{save_id}/current", exist_ok = True)
	os.mkdir(f"./saves/{save_id}/new", exist_ok = True)