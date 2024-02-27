# Jantrack v01
# Zach Jantz
# 2/24/2024
# Store local changes to the jantrack database


class Commits():

    def __init__(self):

        self.shot_additions = []
        self.shot_deletions = []

        self.asset_additions = []
        self.asset_deletions = []


    def record_shot_deletion(self, shot):

        self.shot_deletions.append(shot)

        for asset_record in self.asset_additions:
            if asset_record[0] == shot:
                self.asset_additions.remove(asset_record)

        for deletion in self.asset_deletions:
            if deletion[0] == shot:
                self.asset_deletions.remove(deletion)

        if shot in self.shot_additions:
            self.shot_additions.remove(shot)

    def record_shot_addition(self,shot):

        self.shot_additions.append(shot)

    def record_asset_deletion(self, shot, asset):

        record = [shot,asset]
        self.asset_deletions.append(record)
        if record in self.asset_additions:
            self.asset_additions.remove(record)


    def record_asset_addition(self, shot, asset):

        record = [shot,asset]
        self.asset_additions.append(record)


    def clear_record(self):

        self.shot_additions.clear()
        self.shot_deletions.clear()
        self.asset_additions.clear()
        self.asset_deletions.clear()




