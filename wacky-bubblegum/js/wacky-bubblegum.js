enchant();

STAGE_SIZE = 640;
SPEED = 5;

NORTH = 0;
EAST = 1;
SOUTH = 2;
WEST = 3;

ENEMY_SPAWN_RATE = 60;
GEM_SPAWN_RATE = 90;
GEM_AGE = 120;

MAX_HITS = 3;


function getRandomInt(max) {
    /* Return a random integer between 0 and `max` (inclusive) */
    return Math.floor(Math.random() * (max + 1));
}


Player = Class.create(Sprite, {
    initialize: function () {
        Sprite.call(this, 32, 32);
        this.image = game.assets['img/player.png'];
        this.frame = 7;
        this.scale(2);

        this.x = STAGE_SIZE / 2;
        this.y = STAGE_SIZE / 2;

        this.score = 0;
        this.hits = 0;
    },

    onenterframe: function () {
        if (game.input.left && this.x > 0) {
            this.x -= SPEED;
        }
        if (game.input.right && this.x < STAGE_SIZE - this.width) {
            this.x += SPEED;
        }
        if (game.input.up && this.y > 0) {
            this.y -= SPEED;
        }
        if (game.input.down && this.y < STAGE_SIZE - (1.7 * this.height)) {
            this.y += SPEED;
        }
    }
});


Monster = Class.create(Sprite, {
    initialize: function () {
        Sprite.call(this, 48, 48);
        this.image = game.assets['img/monster.gif'];
        this.frame = 3;

        this.direction = getRandomInt(3);
        switch (this.direction) {
            case NORTH:
                this.x = getRandomInt(STAGE_SIZE);
                this.y = STAGE_SIZE;
                break;
            case EAST:
                this.x = 0;
                this.y = getRandomInt(STAGE_SIZE);
                this.scale(-1, 1);
                break;
            case SOUTH:
                this.x = getRandomInt(STAGE_SIZE);
                this.y = 0;
                this.scale(-1, 1);
                break;
            case WEST:
                this.x = STAGE_SIZE;
                this.y = getRandomInt(STAGE_SIZE);
                break;
        }
        game.currentScene.addChild(this);
    },

    isOnStage: function () {
        return (
            this.x >= 0 &&
            this.x <= STAGE_SIZE &&
            this.y >= 0 &&
            this.y <= STAGE_SIZE
        );
    },

    onenterframe: function () {
        if (!this.isOnStage()) {
            game.currentScene.removeChild(this);
        }

        if (this.intersect(player)) {
            player.hits++;
            game.currentScene.removeChild(this);
        }

        switch (this.direction) {
            case NORTH:
                this.moveBy(0, -SPEED);
                break;
            case EAST:
                this.moveBy(SPEED, 0);
                break;
            case SOUTH:
                this.moveBy(0, SPEED);
                break;
            case WEST:
                this.moveBy(-SPEED, 0);
                break;
        }
    }
});


Gem = Class.create(Sprite, {
    initialize: function () {
        Sprite.call(this, 16, 16);
        this.image = game.assets['img/icons.png'];
        this.frame = 64;
        this.scale(1.3);

        this.x = getRandomInt(STAGE_SIZE);
        this.y = getRandomInt(STAGE_SIZE);
        game.currentScene.addChild(this);
    },

    onenterframe: function () {
        if (this.age > GEM_AGE) {
            game.currentScene.removeChild(this);
        }

        if (this.intersect(player)) {
            player.score++;
            game.currentScene.removeChild(this);
        }
    }
});


ScoreLabel = Class.create(Label, {
    initialize: function () {
        Label.call(this, 'Score: ' + player.score);
        this.font = 'bold 24px UnifrakturCook';
        this.x = 5;
    },

    onenterframe: function () {
        this.text = 'Score: ' + player.score;
    }
});


StartScene = Class.create(Scene, {
    initialize: function () {
        Scene.call(this);
        var start = new Sprite(236, 48);
        start.image = game.assets['img/start.png'];
        start.x = (STAGE_SIZE - start.width) / 2;
        start.y = (STAGE_SIZE - start.height) / 2;
        this.addChild(start);
    },

    ontouchend: function () {
        game.replaceScene(new GameScene());
    }
});


GameOverScene = Class.create(Scene, {
    initialize: function () {
        Scene.call(this);
        var end = new Sprite(189, 97);
        end.image = game.assets['img/end.png'];
        end.x = (STAGE_SIZE - end.width) / 2;
        end.y = (STAGE_SIZE - end.height) / 2;
        this.addChild(end);
        this.addChild(new ScoreLabel());
    },

    ontouchend: function () {
        game.replaceScene(new GameScene());
    }
});


GameScene = Class.create(Scene, {
    initialize: function () {
        Scene.call(this);
        player = new Player();
        this.addChild(player);
        this.addChild(new ScoreLabel());
        new Gem();
    },

    onenterframe: function () {
        if (gameOver()) {
            game.replaceScene(new GameOverScene());
        }

        if (this.age % GEM_SPAWN_RATE === (GEM_SPAWN_RATE / 2)) {
            new Gem();
        }
        if (this.age % ENEMY_SPAWN_RATE === 0) {
            new Monster();
        }
    }
});


var gameOver = function () {
    return player.hits >= MAX_HITS;
};

window.onload = function () {
    game = new Core(STAGE_SIZE, STAGE_SIZE);
    game.preload(
        'img/player.png', 'img/monster.gif', 'img/icons.png',
        'img/start.png', 'img/end.png'
    );
    game.onload = function () {
        game.pushScene(new StartScene());
    };
    game.start();
};
