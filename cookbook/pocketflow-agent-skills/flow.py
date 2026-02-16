from pocketflow import Flow
from nodes import SelectSkill, ApplySkill


def create_flow():
    select_skill = SelectSkill()
    apply_skill = ApplySkill()

    select_skill >> apply_skill

    return Flow(start=select_skill)
