from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models.functions import ExtractYear
from .models import Pesquisador, ProjetoPesquisa, Publicacao, Orientacao, ProducaoGeral, GrupoPesquisa
from django.contrib.auth import logout
import json
import re
from collections import Counter

def is_staff(user):
    return user.is_staff