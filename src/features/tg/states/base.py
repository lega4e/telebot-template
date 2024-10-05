from tgui.src.states.tg_state import TgState

from src.features.tg.domain.user_scope import UserScope


class BaseState(TgState):

  def __init__(self, u: UserScope):
    TgState.__init__(self, destination=u.dst, tg=u.tg)
    self.u = u
