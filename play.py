import falcon
from Puzzle import Puzzle


class Play(object):
    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        paramDefaults = {
            'difficulty': 'hard',
            'level': 1,
            'size': 12
        }
        msg = ''
        for param, default in paramDefaults.items():
            if param not in req.params:
                req.params[param] = default
            msg += param + ': ' + str(req.params[param]) + '\n'

        res.body = (msg)
        return
        # Get the parameters
        # Let it beginp
        # puzzle = Puzzle()
        # puzzle.set(
        #     Puzzle.DIFFICULTY['very hard'],
        #     Puzzle.LEVEL[27],
        #     Puzzle.SIZE['14*14']
        # )
        # puzzle.play()
