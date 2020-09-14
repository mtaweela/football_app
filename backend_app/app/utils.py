from playhouse.shortcuts import model_to_dict
from app.models import (
    db,
    Player,
    Club,
    Nationality,
)

class TeamBuilder(object):
    all_filled = False
    positions = {
        "goalkeeper": ["GK"],
        "fullback": ["LB", "RB", "LWB", "RWB"],
        "halfback": [
            "CB",
            "LCB",
            "RCB",
            "CDM",
            "LDM",
            "RDM",
            "CM",
            "LCM",
            "RCM",
            "LM",
            "RM",
        ],
        "forward_playing": ["CAM", "LAM", "RAM", "LWF", "RWF", "CF", "LCF", "RCF"],
    }
    players_types_dict = {i: k for k, v in positions.items() for i in v}

    goalkeeper_ps = []
    fullback_ps = []
    halfback_ps = []
    forward_playing_ps = []

    def __init__(self, total):
        self.total = total
        self.query = (
            Player.select()
            .where(Player.value <= total / 2)
            .order_by(Player.overall.desc())
        )
        self.query_arr = [model_to_dict(i) for i in self.query]
        self.players_count = self.query.count()

        self.goalkeeper_ps = self._get_goalkeepers()

        self.fullback_ps = self._get_fullback_ps()

        self.halfback_ps = self._get_halfback_ps()

        self.forward_playing_ps = self._get_forward_playing_ps()

        super().__init__()

    def _get_goalkeepers(self):
        query = self.query.where(
            Player.position.in_(self.positions["goalkeeper"])
        ).order_by(Player.overall.desc())
        return [model_to_dict(i) for i in query]

    def _get_fullback_ps(self):
        query = self.query.where(
            Player.position.in_(self.positions["fullback"])
        ).order_by(Player.overall.desc())
        return [model_to_dict(i) for i in query]

    def _get_halfback_ps(self):
        query = self.query.where(
            Player.position.in_(self.positions["halfback"])
        ).order_by(Player.overall.desc())
        return [model_to_dict(i) for i in query]

    def _get_forward_playing_ps(self):
        query = self.query.where(
            Player.position.in_(self.positions["forward_playing"])
        ).order_by(Player.overall.desc())
        return [model_to_dict(i) for i in query]

    def get_team(self):
        current_index = 0
        self._reset()
        while self._is_okay() and current_index < self.players_count:
            self._reset()
            current_index += 1
            item = self.query_arr[0]
            self._remove_item(item)
            self._fill_arr(first_item=item)

        print([i.get("id") for i in self.players_arr])
        print(len(self.players_arr))
        players_arr_total_cost = sum([p.get("value") for p in self.players_arr])
        print("total", f"{players_arr_total_cost:,}")

        if not len(self.players_arr) == 11:
            raise CanNotBuildException()

        return self.players_arr

    def _reset(self):
        self.players_arr = []
        self.goalkeeper_count = 0
        self.fullback_count = 0
        self.halfback_count = 0
        self.forward_playing_count = 0

    def _is_okay(self):
        players_arr_total_cost = sum([p.get("value") for p in self.players_arr])
        return players_arr_total_cost > self.total or len(self.players_arr) < 11

    def _remove_item(self, item):
        self.query_arr.remove(item)
        position = item.get("position")
        ptd = self.players_types_dict[position]
        players_arr = getattr(self, f"{ptd}_ps")
        players_arr.remove(item)

    def _fill_arr(self, first_item):
        ptd = self.players_types_dict[first_item.get("position")]
        current_count = getattr(self, f"{ptd}_count")
        setattr(self, f"{ptd}_count", current_count + 1)
        self.players_arr.append(first_item)

        self._add_goalkeepers()
        self._add_fullbacks()
        self._add_halfbacks()
        self._add_forward_playings()

    def _add_goalkeepers(self):
        if len(self.goalkeeper_ps) < 1:
            raise CanNotBuildException()

        if self.goalkeeper_count < 1:
            self.players_arr.append(self.goalkeeper_ps[0])
            self.goalkeeper_count += 1

    def _add_fullbacks(self):
        if len(self.fullback_ps) < 2:
            raise CanNotBuildException()

        count = 0
        while self.fullback_count < 2:
            self.players_arr.append(self.fullback_ps[count])
            self.fullback_count += 1
            count += 1

    def _add_halfbacks(self):
        if len(self.halfback_ps) < 3:
            raise CanNotBuildException()

        count = 0
        while self.halfback_count < 3:
            self.players_arr.append(self.halfback_ps[count])
            self.halfback_count += 1
            count += 1

    def _add_forward_playings(self):
        if len(self.forward_playing_ps) < 5:
            raise CanNotBuildException()

        count = 0
        while self.forward_playing_count < 5:
            self.players_arr.append(self.forward_playing_ps[count])
            self.forward_playing_count += 1
            count += 1


class CanNotBuildException(Exception):
    message = "Can Not Build Team"

    def __str__(self):
        return self.message
