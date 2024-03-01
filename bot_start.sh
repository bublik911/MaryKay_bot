#!/bin/bash
exec python3 db/models/ClientModel.py &&
exec python3 db/models/ConsultantModel.py &&
exec python3 client_bot.py &&
exec python3 consult_bot.py