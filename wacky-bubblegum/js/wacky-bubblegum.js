enchant();

STAGE_SIZE = 640;
SPEED = 5;

NORTH = 0;
EAST = 1;
SOUTH = 2;
WEST = 3;

ENEMY_SPAWN_RATE = 60;
GEM_SPAWN_RATE = 120;
GEM_MAX_AGE = 120;


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
        game.rootScene.addChild(this);
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
            game.rootScene.removeChild(this);
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
        game.rootScene.addChild(this);
    },

    onenterframe: function () {
        if (this.age > GEM_MAX_AGE) {
            game.rootScene.removeChild(this);
        }
    }
});

window.onload = function () {
    game = new Core(STAGE_SIZE, STAGE_SIZE);
    game.preload('img/player.png', 'img/monster.gif', 'img/icons.png');
    game.onload = function () {
        player = new Player();
        game.rootScene.addChild(player);

        game.rootScene.tl.then(function() {
            var gem = new Gem();
        }).delay(GEM_SPAWN_RATE).loop();

        game.rootScene.tl.then(function() {
            var monster = new Monster();
        }).delay(ENEMY_SPAWN_RATE).loop();
    };
    game.start();
};
