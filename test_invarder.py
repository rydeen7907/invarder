"""

インベーダーっぽいヤツ(試作)

Python3.13.0
Pygame 2.6.1
Gemini Code Assist

"""

import pygame
import random
import sys
import os # ファイルパスの操作用
import math # 角度の計算用

# --- 定数 ---
# 画面設定
WIDTH, HEIGHT = 800, 600
FPS = 30 # フレームレート
CAPTION = "Invarder ?? (Trial)" 
# 画像パスはスクリプトからの相対パスに変更推奨
BACKGROUND_IMAGE_FILENAME = "./image/background.jpg"
# スクリプトのあるディレクトリを取得
BACKGROUND_IMAGE_PATH =  BACKGROUND_IMAGE_FILENAME # 画像パス
script_dir = os.path.dirname(__file__) # 1度書いておくと便利
BACKGROUND_IMAGE_PATH = os.path.join(script_dir, BACKGROUND_IMAGE_FILENAME)
# BGMファイル名を追加
BGM_FILENAME = "./sound/Firecracker.wav" # ここにBGMファイル名を入力
BGM_PATH = os.path.join(script_dir, BGM_FILENAME)
# ゲームオーバーBGMファイル名を追加
GAMEOVER_BGM_FILENAME = "./sound/Computer_Game.mp3" # ここにゲームオーバー用BGMファイル名を入力
GAMEOVER_BGM_PATH = os.path.join(script_dir, GAMEOVER_BGM_FILENAME)
# プレイヤー発射音
PLAYER_SHOOT_SOUND_FILENAME = "./sound/shoot.mp3"
PLAYER_SHOOT_SOUND_PATH = os.path.join(script_dir, PLAYER_SHOOT_SOUND_FILENAME)
# プレイヤー被弾音
PLAYER_HIT_SOUND_FILENAME = "./sound/bomb_1.mp3"
PLAYER_HIT_SOUND_PATH = os.path.join(script_dir, PLAYER_HIT_SOUND_FILENAME)
# UFO破壊音
UFO_EXPLOSION_SOUND_FILENAME = "./sound/bomb_1.mp3"
UFO_EXPLOSION_SOUND_PATH = os.path.join(script_dir, UFO_EXPLOSION_SOUND_FILENAME)
# 弾衝突音
BULLET_CLASH_SOUND_FILENAME = "./sound/bomb_1.mp3"
BULLET_CLASH_SOUND_PATH = os.path.join(script_dir, BULLET_CLASH_SOUND_FILENAME)
# 防護壁点滅音
BARRIER_BLINK_SOUND_FILENAME = "./sound/keikoku.mp3"
BARRIER_BLINK_SOUND_PATH = os.path.join(script_dir, BARRIER_BLINK_SOUND_FILENAME)

# 色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
TRANSPARENT = (0, 0, 0, 0) # 透明(点滅用)

# プレイヤー設定
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 70
PLAYER_SPEED = 7 # 少し速く
PLAYER_LIVES = 3
PLAYER_START_X = WIDTH // 2 - PLAYER_WIDTH // 2
PLAYER_START_Y = HEIGHT - PLAYER_HEIGHT - 10
PLAYER_BULLET_SPEED = -10
PLAYER_MAX_BULLETS = 7 # 画面上の最大弾数
PLAYER_MAX_LIVES = 10 # 最大ライフ数を設定(例)
PLAYER_HIT_MESSAGE_DURATION = 1 * FPS # プレイヤー被弾メッセージ表示時間(1秒)
PLAYER_IMAGE_FILENAME = "./image/missile.png" # プレイヤー画像ファイル
PLAYER_IMAGE_PATH = os.path.join(script_dir, PLAYER_IMAGE_FILENAME)
# デモプレイヤー用設定
DEMO_PLAYER_MOVE_INTERVAL = 1 * FPS # デモプレイヤーが方向転換する間隔
DEMO_PLAYER_FIRE_CHANCE = 15 # デモプレイヤーが弾を撃つ確率 (1/N)

# エイリアン設定
ALIEN_WIDTH = 45
ALIEN_HEIGHT = 30
ALIEN_ROWS = 5
ALIEN_COLS = 10
ALIEN_BASE_SPEED = 1
ALIEN_BASE_DOWN_SPEED = 10
ALIEN_BULLET_SPEED = 5
ALIEN_FIRE_RATE_BASE = 2500 # 発射間隔のベース値 (調整済み)
ALIEN_COLORS = [RED, GREEN, BLUE, YELLOW, CYAN]
ALIEN_SCORES = [10, 7, 5, 3, 1] # 上の行からのスコア
ALIEN_START_Y_BASE = 50
ALIEN_STAGE_Y_OFFSET = 15 # ステージごとのYオフセット
ALIEN_X_GAP = 10
ALIEN_Y_GAP = 10
# エイリアン群全体幅を計算
ALIEN_TOTAL_WIDTH = ALIEN_COLS * ALIEN_WIDTH + (ALIEN_COLS - 1) * ALIEN_X_GAP
# 画面中央に配置するための開始X座標を計算
ALIEN_START_X = (WIDTH - ALIEN_TOTAL_WIDTH) // 2

# UFO設定(1機目)
UFO_WIDTH = 48
UFO_HEIGHT = 48
UFO_Y = 10 
UFO_SPEED = 2
UFO_SPAWN_INTERVAL_MIN = 5 * FPS # 5秒
UFO_SPAWN_INTERVAL_MAX = 12 * FPS # 12秒
UFO_SCORE = 100
# 画像パスはスクリプトからの相対パスに変更推奨
UFO_IMAGE_FILENAME = "./image/Rilakkuma_icon.png"
# スクリプトのあるディレクトリを取得
# script_dir = os.path.dirname(__file__) # すでに定義済み
UFO_IMAGE_PATH = os.path.join(script_dir, UFO_IMAGE_FILENAME)

# UFO設定(2機目・攻撃型)
ATTACKING_UFO_WIDTH = 48
ATTACKING_UFO_HEIGHT = 48
ATTACKING_UFO_Y = 10 
ATTACKING_UFO_SPEED = 3
ATTACKING_UFO_SPAWN_INTERVAL_MIN = 7 * FPS # 7秒
ATTACKING_UFO_SPAWN_INTERVAL_MAX = 20 * FPS # 20秒
ATTACKING_UFO_SCORE = 300
ATTACKING_UFO_FIRE_RATE = 60 # 発射間隔
ATTACKING_UFO_BULLET_SPEED = 7 # 弾の速度
ATTACKING_UFO_BULLET_COLOR = ORANGE # 弾の色
ATTACKING_UFO_IMAGE_FILENAME = "./image/Korilakkuma.png"
ATTACKING_UFO_IMAGE_PATH = os.path.join(script_dir, ATTACKING_UFO_IMAGE_FILENAME)

# UFO設定(3機目・無害型)
PASSIVE_UFO_WIDTH = 96
PASSIVE_UFO_HEIGHT = 72
PASSIVE_UFO_SPEED_MIN = 3 # 最低速度
PASSIVE_UFO_SPEED_MAX = 8 # 最高速度
PASSIVE_UFO_SPAWN_INTERVAL_MIN = 3 * FPS # 5秒
PASSIVE_UFO_SPAWN_INTERVAL_MAX = 12 * FPS # 12秒
PASSIVE_UFO_MAX_COUNT = 3 # 最大出現数
PASSIVE_UFO_IMAGE_FILENAME = "./image/kiiroitori.png"
PASSIVE_UFO_IMAGE_PATH = os.path.join(script_dir, PASSIVE_UFO_IMAGE_FILENAME)

# UFO設定(4機目・ランダム射撃型)
RANDOM_SHOOTER_UFO_WIDTH = 48
RANDOM_SHOOTER_UFO_HEIGHT = 48
RANDOM_SHOOTER_UFO_Y = 10 # 少し下に
RANDOM_SHOOTER_UFO_SPEED = 5
RANDOM_SHOOTER_UFO_SPAWN_INTERVAL_MIN = 10 * FPS # 10秒
RANDOM_SHOOTER_UFO_SPAWN_INTERVAL_MAX = 28 * FPS # 28秒
RANDOM_SHOOTER_UFO_SCORE = 500
RANDOM_SHOOTER_UFO_FIRE_RATE = 45 # 発射間隔
RANDOM_SHOOTER_UFO_BULLET_SPEED = 8 # 弾の速度
RANDOM_SHOOTER_UFO_BULLET_COLOR = YELLOW # 弾の色
RANDOM_SHOOTER_UFO_BULLET_ANGLE_RANGE = 60 # 発射角度の範囲
RANDOM_SHOOTER_UFO_IMAGE_FILENAME = "./image/koguma.png"
RANDOM_SHOOTER_UFO_IMAGE_PATH = os.path.join(script_dir, RANDOM_SHOOTER_UFO_IMAGE_FILENAME)

# 防護壁(バリア)設定
BARRIER_WIDTH = 60
BARRIER_HEIGHT = 40
BARRIER_Y = HEIGHT - PLAYER_HEIGHT - 70 # プレイヤーのミサイルのデザインに合わせてスペースを調整 
BARRIER_COUNT = 5 # 防護壁の数
BARRIER_HEALTH_MAX = 50 # 耐久力
BARRIER_GAP = (WIDTH - BARRIER_WIDTH * BARRIER_COUNT) // (BARRIER_COUNT + 1)
BARRIER_BLINK_THRESHOLD = 1/3 # 点滅を開始する耐久力の割合
BARRIER_BLINK_INTERVAL = 3 # 点滅間隔(フレーム数)

# 弾設定
BULLET_WIDTH = 5
BULLET_HEIGHT = 10

# フォント設定
FONT_NAME = None # デフォルトフォント(設定したフォント次第で日本語対応可能)
FONT_SIZE_NORMAL = 36
FONT_SIZE_LARGE = 48
FONT_SIZE_TITLE = 64

# タイトルスクロール
TITLE_SCROLL_FONT_SIZE = 48
TITLE_SCROLL_SPEED = 1.5 # スクロール速度(px/フレーム)
TITLE_SCROLL_SPACING = 10 # 行間
TITLE_TEXT_COLOR = GREEN # テキストCOLOR
TITLE_TEXT_COLOR_HIGHLIGHT = CYAN
TITLE_TEXT_COLOR_NORMAL = GRAY 

# ゲーム状態
STATE_TITLE = 0       # タイトル表示
STATE_DEMO_PLAY = 1   # デモプレイ
STATE_PLAYING = 2     # プレイ中
STATE_GAME_OVER = 3   # ゲームオーバー
STATE_STAGE_CLEAR = 4 # ステージクリア
TITLE_DURATION = 5 * FPS      # タイトル表示時間 (5秒)
STAGE_CLEAR_DURATION = 3 * FPS # 3秒
GAME_OVER_DURATION = 4 * FPS # 4秒 (ゲームオーバーBGMの長さに合わせる)

# --- Player 定義 ---
class Player(pygame.sprite.Sprite):
    """
    プレイヤーを表すクラス
    """
    def __init__(self, game, is_demo=False):
        """
        Playerオブジェクトを初期化

        Parameters
        ----------
        game : Game
            Gameオブジェクト
        is_demo : bool
            デモモードかどうか
        """
        super().__init__()
        self.game = game
        # is_demo 引数と属性を追加
        self.is_demo = is_demo # デモモードかどうかのフラグ
        
        # プレイヤー画像の読み込み
        self.image = None
        try:
            # 画像をロードしてαチャンネル付きで変換、指定サイズにスケーリング
            loaded_image = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
            self.image = pygame.transform.scale(loaded_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
            print(f"プレイヤー画像の読み込みに成功: {PLAYER_IMAGE_PATH}")
        except pygame.error as e:
            print(f"プレイヤー画像の読み込みに失敗: {e}")
            print(f"パス: {PLAYER_IMAGE_PATH}")
            # 画像読込失敗時のフォールバック
            print ("代替の矩形を使用します") # 例：白い矩形を描画
            self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
            self.image.fill(WHITE)
        # 画像読込処理内に移動    
        # self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        # self.image.fill(WHITE)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = PLAYER_START_X + PLAYER_WIDTH // 2
        self.rect.bottom = PLAYER_START_Y + PLAYER_HEIGHT
        self.speed_x = 0
        self.lives = PLAYER_LIVES
        self.last_shot_time = 0 # 連射制御用（今回は未使用だが将来的に）
        # デモ用属性
        self.demo_move_timer = 0
        self.demo_move_direction = random.choice([-1, 1]) # 初期移動方向
    
    def update(self):
        """
        プレイヤーの状態を更新する

        デモモードでは、自動的に移動し、時々弾を撃つ
        通常のプレイヤー操作では、左右キーで移動する
        画面端での移動制限も行う
        """
        # デモモードと通常モードで処理分岐
        if self.is_demo:
            # デモプレイヤーの自動操作
            self.demo_move_timer += 1
            # 移動方向転換判定
            if self.demo_move_timer >= DEMO_PLAYER_MOVE_INTERVAL or \
               (self.rect.left <= 0 and self.demo_move_direction == -1) or \
               (self.rect.right >= WIDTH and self.demo_move_direction == 1):
                self.demo_move_direction *= -1 # 方向転換
                self.demo_move_timer = 0 # タイマーリセット

            self.speed_x = PLAYER_SPEED * self.demo_move_direction

            # 自動射撃判定
            if random.randint(1, DEMO_PLAYER_FIRE_CHANCE) == 1:
                self.shoot()
        else:
            #  通常のプレイヤー操作
            self.speed_x = 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.speed_x = -PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                self.speed_x = PLAYER_SPEED

        # 共通の移動処理
        self.rect.x += self.speed_x
        # 画面端での移動制限
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH      
      
    def shoot(self):
        # 画面上の弾数を制限
        """
        プレイヤーが弾を撃つ
        画面上に PLAYER_MAX_BULLETS 数以下の弾が存在する場合に、新しい弾を生成する
        """
        if len(self.game.player_bullets) < PLAYER_MAX_BULLETS:
            # サウンドエフェクトを追加
            if self.game.player_sound_loaded:
                self.game.player_sound.play()
            bullet = Bullet(self.rect.centerx, self.rect.top, PLAYER_BULLET_SPEED, WHITE)
            self.game.all_sprites.add(bullet)
            self.game.player_bullets.add(bullet)

    def hit(self):
        """
        プレイヤーがエイリアンの弾に当たったときのイベントを処理

        通常のゲームプレイでは、プレイヤーのライフ数を減らし、
        ゲームに被弾メッセージとタイマーを設定。
        
        プレイヤーのライフがまだ残っている場合は、プレイヤーの位置をリセット
        ライフが0になった場合のゲームオーバー条件は、Gameクラスによって処理

        デモモードでは、デモプレイヤーがヒットされたときに、
        デモプレイのリセットをトリガーする
        """
        #  デモ中はゲームオーバーにしない
        if not self.is_demo:
            # 被弾サウンドエフェクトを追加
            if self.game.player_hit_sound_loaded:
                self.game.player_hit_sound.play()
            
            self.lives -= 1
            if self.lives > 0:    
                # メッセージとタイマーをGameオブジェクトに設定
                self.game.player_hit_message = f"Player hit! Lives: {self.lives}"
                self.game.player_hit_message_timer = PLAYER_HIT_MESSAGE_DURATION
                # プレイヤーの位置をリセット
                self.rect.centerx = PLAYER_START_X + PLAYER_WIDTH // 2
                self.rect.bottom = PLAYER_START_Y + PLAYER_HEIGHT
                pass
            # ライフが0になった場合のゲームオーバー判定は Game クラスで行う
        else:
            # デモプレイヤーがヒットした場合（デモプレイリセットのトリガー）
            print("Demo player hit!")
            self.game.trigger_demo_reset = True # デモプレイリセットフラグを立てる

# --- Alien 定義 ---
class Alien(pygame.sprite.Sprite):
    """
    エイリアンを表すクラス
    """
    def __init__(self, x, y, color, score, speed, down_speed):
        """
        エイリアンを初期化

        Parameters
        ----------
        x, y : int
            エイリアンの左上座標
        color : tuple
            エイリアンの色 (RGB)
        score : int
            エイリアンのスコア
        speed : int
            エイリアンの水平スピード
        down_speed : int
            エイリアンの垂直スピード
        """
        super().__init__()
        self.image = pygame.Surface((ALIEN_WIDTH, ALIEN_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.score = score
        self.speed_x = speed
        self.speed_y = down_speed
        self.direction = 1 # 1:右, -1:左

    def update(self, move_down=False): # move_down=True:下へ移動
        """
        エイリアンの位置を更新

        Parameters
        ----------
        move_down : bool, optional
            下方向に移動するか (default: False)
        """
        self.rect.x += self.speed_x * self.direction
        if move_down:
            self.rect.y += self.speed_y

    def reverse_direction(self):
        """
        エイリアンの水平移動方向を反転させます。

        現在の移動方向に-1を掛けることでエイリアンの水平移動方向を変更
        画面端付近でのブレ（ちらつき）を防ぐため、エイリアンを新しい方向にわずかに移動させる
        """
        self.direction *= -1
        # 壁際での震え防止のため、少し逆方向に動かす
        self.rect.x += 2 * self.direction # 速度にかかわらず、2px移動
        
# --- Bullet 定義 ---        
class Bullet(pygame.sprite.Sprite):
    """
    弾を表すクラス (プレイヤー・エイリアン・攻撃型UFO・ランダム射撃型共通)
    """
    # 波状弾のパラメータ
    WAVE_AMPLITUDE = 3 # 波の振幅
    WAVE_FREQUENCY = 3 # 波の周波数

    # is_wave 引数を追加
    def __init__(self, x, y, speed_y, color,speed_x=0, is_wave=False): # is_wave=True:波状弾
        """
        弾を初期化

        Parameters
        ----------
        x, y : int
            弾の左上座標
        speed_y : int
            弾の垂直スピード
        color : tuple
            弾の色 (RGB)    
        speed_x : float or int, optional
            弾の水平スピード (default: 0)
        is_wave : bool, optional
            波状弾フラグ (default: False)

        Notes
        -----
        speed_xが指定されると水平方向にも移動する
        is_wave=True の場合、x座標を波状に動かす(speed_xとの併用に注意)
        """
        super().__init__()
        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        # 弾の発射位置の条件分岐を修正
        if speed_y < 0: # プレイヤー弾 (上向き、速度が負)
            self.rect.bottom = y
        else: # エイリアン弾 or 攻撃型UFO (下向き、速度が正)
            self.rect.top = y
        
        # 速度は浮動小数点数で保持し、移動時に整数に変換するほうが滑らか
        self.exact_x = float(self.rect.centerx)
        self.exact_y = float(self.rect.y)
        self.speed_x = float(speed_x) # speed_xを保存
        self.speed_y = float(speed_y)
        
        # 初期位置と経過距離を保存
        self.initial_x = x
        self.initial_y = self.rect.y # 発射時のy座標を保存
        self.is_wave = is_wave # 波状弾フラグ
        

    def update(self):
        # y座標は常に直線的に移動
        """
        弾を更新
        
        speed_x, speed_yに基づいて移動
        
        is_wave フラグがTrueでかつ下向きの場合、
        x座標を波状に動かす

        画面外に出たら削除
        """
        # 座標を浮動小数点数で更新
        self.exact_x += self.speed_x
        self.exact_y += self.speed_y
        
        # 整数に変換してrect座標を更新
        self.rect.centerx = int(self.exact_x)
        self.rect.y += self.speed_y
        
        # is_wave フラグで波状移動を制御
        # speed_x = 0でない場合でも is_wave = True なら波状にするか排他にするか？
        # is_wave = True なら波状にする
        if self.is_wave and self.speed_y > 0: # 波状弾フラグがTrueでかつ下向き
            # 発射地点からy方向の移動距離を計算
            distance_y = self.rect.y - self.initial_y
            # sin関数を用いてx座標を計算(初期位置からのオフセットとして計算)
            offset_x = self.WAVE_AMPLITUDE * math.sin(distance_y / self.WAVE_FREQUENCY)
            # speed_x による移動とは別に、初期位置からのオフセットとして計算する
            # 注意：speed_xによる移動と is_wave による移動が混在すると複雑になる
            #   ランダム角度弾は is_wave = False
            #   波状弾は is_wave = speed_x = 0
            self.rect.centerx = int(self.initial_x + offset_x)
            self.exact_x = self.initial_x + offset_x # exact_xも更新
        
        # エイリアン弾の場合、x座標を波状に動かす
        # if self.is_wave and self.speed_y > 0: # 波状弾フラグがTrueでかつ下向き
            # 発射地点からy方向の移動距離を計算
            # distance_y = self.rect.y - self.initial_y
            # sin関数を用いてx座標を計算
            # offset_x = self.WAVE_AMPLITUDE * math.sin(distance_y / self.WAVE_FREQUENCY)
            # self.rect.centerx = self.initial_x + offset_x
        
        # 画面外に出たら削除
        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill() # スプライトグループから自動的に削除

# --- Barrier定義 ---
class Barrier(pygame.sprite.Sprite):
    """
    防護壁を表すクラス
    """
    def __init__(self, x, y, game):
        """
        x, y:  Barrierの左上座標
        super().__init__()でSpriteの初期化を行う
        Gameオブジェクトへの参照を保持
        health:  Barrierの耐久力
        max_health:  Barrierの最大耐久力
        image:  Surfaceオブジェクト (SRCALPHAフラグあり)
        rect:  Rectオブジェクト
        is_blinking:  Barrierが点滅状態にあるか否かのフラグ
        blink_timer:  Barrierの点滅タイマー
        visible:  Barrierが表示状態にあるか否かのフラグ
        was_blinking_before:  前フレームでの点滅状態フラグ
        _update_image(): Barrierの初期色を設定
        """
        super().__init__()
        self.game = game # Gameオブジェクトへの参照を保持
        self.health = BARRIER_HEALTH_MAX
        self.max_health = BARRIER_HEALTH_MAX
        # SRCALPHAフラグを追加して透明度を扱えるようにする
        self.image = pygame.Surface((BARRIER_WIDTH, BARRIER_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_blinking = False # 点滅状態フラグ
        self.blink_timer = 0 # 点滅タイマー
        self.visible = True # 表示状態フラグ
        self.was_blinking_before = False # 前フレームの点滅していたかのフラグ
        self._update_image() # 初期色を設定

    # Barrier の update メソッド
    # Barrier の状態（点滅など）は毎フレーム更新する必要がある
    def update(self):
        """
        バリアの状態を更新

        各フレームごとにバリアの外観を更新するために呼び出され、
        バリアの耐久力に応じた色や点滅状態を設定
        """
        self._update_image()

    def _update_image(self):
        """
        耐久力に応じて色を更新
        1/2で点灯、残りわずかで点滅
        """
        if self.health <= 0:
            # kill() は hit() または alien_touch() で呼ばれるのでここでは不要
            return
        
        # 前フレームの点滅状態を保存 (was_blinking_before を self.was_blinking_before に)
        was_blinking_before = self.is_blinking
        
        health_ratio = self.health / self.max_health

        # 色の決定と点滅フラグの設定
        if health_ratio < BARRIER_BLINK_THRESHOLD: # 点滅閾置と比較
            color = RED
            self.is_blinking = True # 耐久力が閾値未満になったら点滅開始
        elif health_ratio < 2/3:
            color = YELLOW
            self.is_blinking = False # 点滅停止
            self.visible = True # 点滅が終わったら必ず表示状態に戻す
        else:
            # 耐久力に応じて灰色から白っぽく変化
            r = int(GRAY[0] * health_ratio + WHITE[0] * (1 - health_ratio))
            g = int(GRAY[1] * health_ratio + WHITE[1] * (1 - health_ratio))
            b = int(GRAY[2] * health_ratio + WHITE[2] * (1 - health_ratio))
            base_color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))) # 0-255の範囲に収める
            color = base_color
            self.is_blinking = False # 点滅停止
            self.visible = True # 点滅が終わったら必ず表示状態に戻す
            
        # 点滅状態の変化を検知してGameのカウンターで操作 
        if not was_blinking_before and self.is_blinking:
            self.game.increment_blinking_barrier()
        elif was_blinking_before and not self.is_blinking:
            self.game.decrement_blinking_barrier()
            
        # 点滅処理
        if self.is_blinking:
            self.blink_timer += 1
            if self.blink_timer >= BARRIER_BLINK_INTERVAL:
                self.visible = not self.visible # 表示状態を切換
                self.blink_timer = 0 # タイマーリセット

            if self.visible:
                # 表示状態：決定した色で塗りつぶす
                self.image.fill(color)
            else:
                # 非表示状態：透明にする(SRCALPHA)
                self.image.fill(TRANSPARENT) # RGBAで完全に透明
        else:
            # 点滅していない場合は常に表示、決定した色で塗りつぶす
            self.image.fill(color)

    def hit(self, damage=1):
        """
        弾が当たった時の処理
        """
        if self.health > 0: # すでに破壊されていない場合のみ
            self.health -= damage
            if self.health <= 0:
                self.health = 0 # 0未満にならないように
                # 破戒される前に点滅中ならカウンターを減らす
                if self.is_blinking:
                    self.game.decrement_blinking_barrier()            
                self.kill() # 耐久力がなくなったら消滅
            # else: # _update_image は update() で呼ばれるのでここでは不要かも
            #     self._update_image()

    def alien_touch(self):
        """
        エイリアンが触れた時の処理（即破壊）
        """
        # 破戒される前に点滅中ならカウンターを減らす
        if self.is_blinking:
            self.game.decrement_blinking_barrier()
        
        self.health = 0
        self.kill()

# --- 通常型UFO 定義 ---
class UFO(pygame.sprite.Sprite):
    """
    UFOを表すクラス(通常型)
    """
    def __init__(self):
        super().__init__()
        self.image = None
        self.load_image() # 画像読み込み試行
        if self.image is None: # 読み込めなかった場合
            self.image = pygame.Surface((UFO_WIDTH, UFO_HEIGHT))
            self.image.fill(MAGENTA) # 通常はマゼンタ
        self.rect = self.image.get_rect()
        # UFOの出現方向をランダムに
        if random.choice([True, False]):
            self.rect.right = 0 # 左から出現
            self.speed_x = UFO_SPEED
        else:
            self.rect.left = WIDTH # 右から出現
            self.speed_x = -UFO_SPEED
        self.rect.y = UFO_Y

    def load_image(self):
        """
        UFOの画像をロード

        画像パス: `UFO_IMAGE_PATH`
        読み込み失敗時はマゼンタ色の矩形を使用
        """
        try:
            self.image = pygame.image.load(UFO_IMAGE_PATH).convert_alpha()
            self.image = pygame.transform.scale(self.image, (UFO_WIDTH, UFO_HEIGHT))
        except pygame.error as e:
            print(f"UFO画像の読み込みに失敗: {e}")
            print(f"パス: {UFO_IMAGE_PATH}")
            self.image = None

    def update(self):
        """
        UFOを更新

        x座標を水平方向スピード分移動

        画面外に出たら削除
        """
        self.rect.x += self.speed_x
        # 画面外に出たら削除
        if self.speed_x > 0 and self.rect.left > WIDTH: # 右へ移動中
            self.kill()
        elif self.speed_x < 0 and self.rect.right < 0: # 左へ移動中
            self.kill()
            
# --- AttackingUFO クラス ---
class AttackingUFO(pygame.sprite.Sprite):
    """
    攻撃型UFOを表すクラス
    """
    def __init__(self, game): # Gameオブジェクトを受け取るように変更
        """
        攻撃型UFOを初期化

        Parameters
        ----------
        game : Game
            Gameオブジェクト

        Notes
        -----
        画像をロードし、出現位置をランダムに設定
        """
        super().__init__()
        self.game = game # Gameオブジェクトを保持
        self.image = None
        self.load_image() # 画像読み込み試行
        if self.image is None: # 読み込めなかった場合
            self.image = pygame.Surface((ATTACKING_UFO_WIDTH, ATTACKING_UFO_HEIGHT))
            self.image.fill(CYAN) # 攻撃UFOはシアン (画像がない場合)
        self.rect = self.image.get_rect()
        # 出現方向をランダムに
        if random.choice([True, False]):
            self.rect.right = 0 # 左から出現
            self.speed_x = ATTACKING_UFO_SPEED
        else:
            self.rect.left = WIDTH # 右から出現
            self.speed_x = -ATTACKING_UFO_SPEED
        self.rect.y = ATTACKING_UFO_Y
        self.fire_timer = 0 # 発射タイマー

    def load_image(self):
        """
        攻撃型UFOの画像をロード

        このメソッドは、指定された ATTACKING_UFO_IMAGE_PATH から画像をロード
        成功した場合、画像を攻撃型UFOに適したサイズにスケーリング
        失敗した場合、image 属性を None に設定し、エラーをログに出力

        注意事項
        -----
        色の調整が必要な場合は、ロードされた画像に対して
        色合いの適用などの追加処理を実行可能
        """
        try:
            # 既存のUFOと同じ画像パスを使用
            self.image = pygame.image.load(ATTACKING_UFO_IMAGE_PATH).convert_alpha()
            self.image = pygame.transform.scale(self.image, (ATTACKING_UFO_WIDTH, ATTACKING_UFO_HEIGHT))
            # 必要であれば色を変えるなどの処理を追加 (例: 赤みがける)
            # tint_color = (255, 100, 100, 100) # 半透明の赤
            # tint_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            # tint_surface.fill(tint_color)
            # self.image.blit(tint_surface, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        except pygame.error as e:
            print(f"攻撃UFO画像の読み込みに失敗: {e}")
            print(f"パス: {ATTACKING_UFO_IMAGE_PATH}")
            self.image = None

    def update(self):
        """
        攻撃型UFOの位置と発射ロジックを更新

        このメソッドは、攻撃型UFOをその速度に応じて水平方向に移動させ
        UFOが画面外に出た場合、削除される
        さらに、発射タイマーを確認し、タイマーが設定された発射間隔に達したら
        UFOに弾を発射させ、その後タイマーをリセットする
        """
        self.rect.x += self.speed_x
        # 画面外に出たら削除
        if self.speed_x > 0 and self.rect.left > WIDTH: # 右へ移動中
            self.kill()
        elif self.speed_x < 0 and self.rect.right < 0: # 左へ移動中
            self.kill()

        # 発射判定
        self.fire_timer += 1
        if self.fire_timer >= ATTACKING_UFO_FIRE_RATE:
            self.shoot()
            self.fire_timer = 0 # タイマーリセット

    def shoot(self):
        # 攻撃UFOの弾を発射
        # Bulletクラスの is_wave を False にして直線弾にする
        """
        攻撃型UFOから弾を発射

        このメソッドは、攻撃型UFOの矩形の中心下部に、指定された速度と色で
        下向きに移動する新しい弾インスタンスを作成
        弾は、描画と衝突判定のために、
        ゲームの all_sprites および attacking_ufo_bullets グループに追加される
        弾は、is_wave プロパティが False に設定されているため、直線的に発射される
        """

        bullet = Bullet(self.rect.centerx, self.rect.bottom, ATTACKING_UFO_BULLET_SPEED, ATTACKING_UFO_BULLET_COLOR, is_wave=False)
        self.game.all_sprites.add(bullet)
        self.game.attacking_ufo_bullets.add(bullet) # 専用の弾グループに追加

# --- PassiveUFO クラス ---
class PassiveUFO(pygame.sprite.Sprite):
    """
    パッシブ(無害な)UFOを表すクラス
    ランダムに飛び回るだけ
    """
    def __init__(self):
        """
        Initialize a PassiveUFO instance.
        PassiveUFOを初期化
        画像をロードし、画面内のランダムな位置・速度で飛行
        曲線移動用のパラメータも初期化
        
        Parameters
        ----------
        x, y : int
            The initial position of the PassiveUFO
        """
        super().__init__()
        self.image = None
        self.load_image() # 画像読み込み試行
        if self.image is None: # 読み込めなかった場合
            self.image = pygame.Surface((PASSIVE_UFO_WIDTH, PASSIVE_UFO_HEIGHT),pygame.SRCALPHA) # 透明背景に
            self.image.fill(GRAY + (180,)) # 通常はグレー+α(透明度)
            # もしくは単純な色での塗りつぶし
            # self.image = pygame.Surface((PASSIVE_UFO_WIDTH, PASSIVE_UFO_HEIGHT))
            # self.image.fill(GRAY) 
        self.rect = self.image.get_rect()
        
        # 画面上半分内のランダムな位置に出現(引数を使わないように戻す)
        self.rect.x = random.randint(0, WIDTH - PASSIVE_UFO_WIDTH)
        self.rect.y = random.randint(0, HEIGHT // 2 - PASSIVE_UFO_HEIGHT) # 上半分
        
        # ランダムな速度ベクトルを設定
        # speed = random.randint(PASSIVE_UFO_SPEED_MIN, PASSIVE_UFO_SPEED_MAX) # 整数速度
        speed = random.uniform(PASSIVE_UFO_SPEED_MIN, PASSIVE_UFO_SPEED_MAX) # 浮動小数点数速度
        angle = random.uniform(0, 2 * math.pi) # 0から2πまでのランダムな角度
        self.base_speed_x = math.cos(angle) * speed
        self.base_speed_y = math.sin(angle) * speed
        
        # 曲線移動用パラメータ
        self.curve_timer = random.uniform(0, 2 * math.pi) # 開始位相をランダムに
        
        # x方向の揺らぎ(sin)
        self.curve_amplitude_x = random.uniform(0.5, 1.5) # 揺らぎの大きさ
        self.curve_frequency_x= random.uniform(0.02, 0.8) # 揺らぎの速さ(周波数) - 少し遅めに調整
        
        # y方向の揺らぎ(cos xと位相をずらす)
        self.curve_amplitude_y = random.uniform(0.5, 1.5)
        self.curve_frequency_y = random.uniform(0.02, 0.8)

        # 実際の移動に使う座標は浮動小数点数で保持
        self.exact_x = float(self.rect.x)
        self.exact_y = float(self.rect.y)


    def load_image(self):
        """
        PassiveUFOの画像をロード
        失敗した場合は None を返す        
        """
        try:
            loaded_image = pygame.image.load(PASSIVE_UFO_IMAGE_PATH).convert_alpha()
            self.image = pygame.transform.scale(loaded_image, (PASSIVE_UFO_WIDTH, PASSIVE_UFO_HEIGHT))
        except pygame.error as e:
            print(f"パッシブUFO画像の読み込みに失敗: {e}")
            print(f"パス: {PASSIVE_UFO_IMAGE_PATH}")
            self.image = None
            
    def update(self):
        """
        PassiveUFOの位置を更新
        直線移動に曲線的な揺らぎを追加
        画面端で跳ね返る
        たまに基本速度方向をランダムに変える
        """
        # 曲線タイマーを更新
        self.curve_timer += 1
        
        # 曲線移動の計算
        # x方向の揺らぎ(sin)
        offset_x = self.curve_amplitude_x * math.sin(self.curve_timer * self.curve_frequency_x)
        # y方向の揺らぎ(cos sinと位相がずれる)
        offset_y = self.curve_amplitude_y * math.cos(self.curve_timer * self.curve_frequency_y)
        
        # 座標の更新
        # 基本速度による直線移動 + 曲線オフセット
        self.exact_x += self.base_speed_x + offset_x
        self.exact_y += self.base_speed_y + offset_y
        
        # rect座標を更新
        self.rect.x = int(self.exact_x)
        self.rect.y = int(self.exact_y)
        
        # 画面端で跳ね返る
        bounce_occurred = False
        if self.rect.left < 0:
            self.rect.left = 0
            self.exact_x = float(self.rect.x) # exact_x 座標も補正
            self.base_speed_x *= -1 # 基本速度を反転
            bounce_occurred = True
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.exact_x = float(self.rect.x)
            self.base_speed_x *= -1
            bounce_occurred = True
            
        if self.rect.top < 0:
            self.rect.top = 0
            self.exact_y = float(self.rect.y) # exact 座標も補正
            self.base_speed_y *= -1
            bounce_occurred = True
        elif self.rect.bottom > HEIGHT: # 画面下端でも跳ね返るように修正
            self.rect.bottom = HEIGHT
            self.exact_y = float(self.rect.y) # exact 座標も補正
            self.base_speed_y *= -1
            bounce_occurred = True
        
        # 画面端で跳ね返った場合、揺らぎの位相もリセット(任意)    
        if bounce_occurred:
            self.curve_timer = random.uniform(0, 2 * math.pi)
        
        # オプション：たまに方向をランダムに変える
        if random.randint(0, 200) == 0: # 1/201フレームの確率で変更
            # 現在の速度の大きさを維持
            current_spped_magnitude = math.sqrt(self.base_speed_x ** 2 + self.base_speed_y ** 2)
            # 新しいランダムな角度
            angle = random.uniform(0, 2 * math.pi)
            # 新しい基本速度ベクトルを設定
            self.base_speed_x = math.cos(angle) * current_spped_magnitude
            self.base_speed_y = math.sin(angle) * current_spped_magnitude
            # print("Passive UFO changed direction!") # デバッグ用
            
class RandomShooterUFO(pygame.sprite.Sprite):
    """
    RandomShooterUFO クラス
    """
    def __init__(self,game): # Game引数を追加
        """
        ランダム射撃型UFOを初期化
        
        Parameters
        ----------
        game : Game
            Game オブジェクト
            
        Notes
        -----
        画像をロードし、出現位置をランダムに設定
        指定された範囲内のランダムな下向き角度で発射
        """
        super().__init__()
        self.game = game # Gameオブジェクトを保持
        self.image = None
        self.load_image() # 画像読み込み試行
        if self.image is None: # 読み込めなかった場合
            # 定義した定数を使うよう設定
             self.image = pygame.Surface(RANDOM_SHOOTER_UFO_WIDTH, RANDOM_SHOOTER_UFO_HEIGHT)
             self.image.fill(YELLOW) # 定義した色を使う 
        self.rect = self.image.get_rect()
        
        # 出現方向をランダムに
        if random.choice([True, False]):
            self.rect.right = 0 # 左から出現
            self.speed_x = RANDOM_SHOOTER_UFO_SPEED
        else:
            self.rect.left = WIDTH # 右から出現
            self.speed_x = -RANDOM_SHOOTER_UFO_SPEED
            
        self.rect.y = RANDOM_SHOOTER_UFO_Y
        self.fire_timer = 0 # 発射タイマー
        
    def load_image(self):
        """
        RandomShooterUFOの画像をロード
        失敗した場合は None を返す
        """
        try:
            loaded_image = pygame.image.load(RANDOM_SHOOTER_UFO_IMAGE_PATH).convert_alpha()
            self.image = pygame.transform.scale(loaded_image, (RANDOM_SHOOTER_UFO_WIDTH, RANDOM_SHOOTER_UFO_HEIGHT))
        except pygame.error as e:
            print(f"ランダム射撃型UFO画像の読み込みに失敗: {e}")
            print(f"パス: {RANDOM_SHOOTER_UFO_IMAGE_PATH}")
            self.image = None
            
    def update(self):
        """
        RandomShooterUFOの位置と発射ロジックを更新
        """
        self.rect.x += self.speed_x
        # 画面外に出たら削除
        if self.speed_x > 0 and self.rect.left > WIDTH: # 右へ移動中
            self.kill()
        elif self.speed_x < 0 and self.rect.right < 0: # 左へ移動中
            self.kill()
        
        # 発射判定
        self.fire_timer += 1
        if self.fire_timer >= RANDOM_SHOOTER_UFO_FIRE_RATE:
            self.shoot()
            self.fire_timer = 0 # タイマーリセット
            
    def shoot(self):
        """
        下方向ランダムな角度で弾を発射
        """
        # 下方向ランダムな角度を決定(真下90度 +/- ANGLE_RANGE)
        min_angle = 90 - RANDOM_SHOOTER_UFO_BULLET_ANGLE_RANGE
        max_angle = 90 + RANDOM_SHOOTER_UFO_BULLET_ANGLE_RANGE
        angle_degrees = random.uniform(min_angle, max_angle)
        angle_radians = math.radians(angle_degrees)
        
        # 速度ベクトルを計算
        bullet_speed_x = math.cos(angle_radians) * RANDOM_SHOOTER_UFO_BULLET_SPEED
        # Y軸は下向きが正なので、sinの結果をそのまま使う
        bullet_speed_y = math.sin(angle_radians) * RANDOM_SHOOTER_UFO_BULLET_SPEED
        
        # Bulletインスタンスを生成(speed_xを返す)
        bullet = Bullet(
            self.rect.centerx, 
            self.rect.bottom, # 発射元 Y座標
            bullet_speed_y, # 計算した Y速度
            RANDOM_SHOOTER_UFO_BULLET_COLOR,
            speed_x=bullet_speed_x, # 計算した X速度
            is_wave=True # False = 直線弾
        )
        self.game.all_sprites.add(bullet)
        # 専用の弾グループに追加(Gameクラスで定義)
        self.game.random_shooter_ufo_bullets.add(bullet)
        # 発射音
        # if self.game.random_shooter_ufo_shoot_sound_loaded:
        #     self.game.random_shooter_ufo_shoot_sound.play()
        
# --- Particle クラス ---
class Particle(pygame.sprite.Sprite):
    """
    パーティクルを表すクラス
    """
    def __init__(self, x, y):
        """
        パーティクルを初期化

        Parameters
        ----------
        x, y : int
            パーティクルの中心座標

        Notes
        -----
        画像をロードし、サイズと色をランダムに設定
        """
        super().__init__()
        self.size = random.randint(2, 5)
        self.image = pygame.Surface((self.size, self.size))
        # 色の選択肢をリストで渡す
        color = random.choice([YELLOW, RED, CYAN, MAGENTA, GREEN, ORANGE])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center =(x, y)

        # 速度をランダムな方向に設定
        angle = random.uniform(0, 2 * math.pi) # 0から2πまでのランダムな角度
        speed = random.uniform(1, 5) # 1から5までのランダムな速度
        self.speed_x = math.cos(angle) * speed
        self.speed_y = math.sin(angle) * speed

        self.gravity = 0.15 # 重力加速度
        self.friction = 0.98 # 空気抵抗/摩擦
        self.lifetime = random.randint(15, 35) # 生存期間

    def update(self):
        # 重力加速度
        """
        粒子の状態(パーティクルの速度)を更新

        粒子の垂直速度に重力を適用し、水平および垂直速度に摩擦を適用し、
        粒子の位置を速度に基づいて更新し、その寿命を減少させる
        粒子の寿命がゼロ以下になると、ゲームから削除される
        """
        self.speed_y += self.gravity
        # 摩擦
        self.speed_x *= self.friction
        self.speed_y *= self.friction
        # 移動
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # 寿命を減らす
        self.lifetime -= 1 # 寿命を減らす処理を追加
        if self.lifetime <= 0:
            self.kill()

# --- Game クラス ---
class Game:
    """
    ゲーム全体を管理するクラス
    """
    def __init__(self):
        """
        ゲームを初期化

        pygameライブラリを初期化し、表示モード、キャプション、フォントオブジェクトを設定
        背景画像とBGM（利用可能な場合）を読み込み、ゲーム状態、スコア、ステージ、タイマーなどの
        他のゲーム関連の属性を初期化
        最後に、プレイヤー、エイリアン、弾丸、バリア、UFO、粒子のためのスプライトグループを作成
        """
        pygame.init()
        pygame.mixer.init() # サウンド用に初期化
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.font_normal = pygame.font.Font(FONT_NAME, FONT_SIZE_NORMAL)
        self.font_large = pygame.font.Font(FONT_NAME, FONT_SIZE_LARGE)
        self.font_title = pygame.font.Font(FONT_NAME, FONT_SIZE_TITLE)
        self.running = True
        # 背景画像の読込処理を追加
        self.background_image = None 
        try:
        #    # 背景画像を読込み、画面サイズにスケーリングし、描画用に変換
           loaded_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
           self.background_image = pygame.transform.scale(loaded_image, (WIDTH, HEIGHT))
           print(f"背景画像の読み込みに成功: {BACKGROUND_IMAGE_PATH}")
        except pygame.error as e:
           print(f"背景画像の読み込みに失敗: {e}")
           print(f"パス: {BACKGROUND_IMAGE_PATH}")
        # 読み込めなかった場合は None のまま
        
        # BGM読み込み処理を追加
        self.bgm_loaded = False
        try:
            pygame.mixer.music.load(BGM_PATH)
            pygame.mixer.music.set_volume(0.5) # 音量を50%に設定 (0.0 ~ 1.0)
            self.bgm_loaded = True
            print(f"BGMの読み込みに成功: {BGM_PATH}")
        except pygame.error as e:
            print(f"BGMの読み込みに失敗: {e}")
            print(f"パス: {BGM_PATH}")
            
         # ゲームオーバーBGM読み込み処理を追加
        self.gameover_sound = None
        self.gameover_sound_loaded = False
        try:
            self.gameover_sound = pygame.mixer.Sound(GAMEOVER_BGM_PATH)
            self.gameover_sound.set_volume(1.0) # サウンドの音量を100%に設定
            self.gameover_sound_loaded = True
            print(f"ゲームオーバーBGMの読み込みに成功: {GAMEOVER_BGM_PATH}")
        except pygame.error as e:
            print(f"ゲームオーバーBGMの読み込みに失敗: {e}")
            print(f"パス: {GAMEOVER_BGM_PATH}")
            
        # プレイヤーサウンドエフェクトを追加
        self.player_sound = None
        self.player_sound_loaded = False
        try:
            self.player_sound = pygame.mixer.Sound(PLAYER_SHOOT_SOUND_PATH)
            self.player_sound.set_volume(0.8) # サウンドの音量を80%に設定
            self.player_sound_loaded = True
            print(f"サウンドの読み込みに成功: {PLAYER_SHOOT_SOUND_PATH}")
        except pygame.error as e:
            print(f"サウンドの読み込みに失敗: {e}")
            print(f"パス: {PLAYER_SHOOT_SOUND_PATH}")
            
        # プレイヤー被弾サウンドエフェクトを追加
        self.player_hit_sound = None
        self.player_hit_sound_loaded = False
        try:
            self.player_hit_sound = pygame.mixer.Sound(PLAYER_HIT_SOUND_PATH)
            self.player_hit_sound.set_volume(1.0) # サウンドの音量を100%に設定
            self.player_hit_sound_loaded = True
            print(f"サウンドの読み込みに成功: {PLAYER_HIT_SOUND_PATH}")
        except pygame.error as e:
            print(f"サウンドの読み込みに失敗: {e}")
            print(f"パス: {PLAYER_HIT_SOUND_PATH}")
        
        # UFOサウンドエフェクトを追加
        self.ufo_explosion_sound = None
        self.ufo_explosion_sound_loaded = False
        try:
            self.ufo_explosion_sound = pygame.mixer.Sound(UFO_EXPLOSION_SOUND_PATH)
            self.ufo_explosion_sound.set_volume(1.0) # サウンドの音量を100%に設定
            self.ufo_explosion_sound_loaded = True
            print(f"UFOサウンドの読み込みに成功: {UFO_EXPLOSION_SOUND_PATH}")    
        except pygame.error as e:
            print(f"UFOサウンドの読み込みに失敗: {e}")
            print(f"パス: {UFO_EXPLOSION_SOUND_PATH}")
            
        # 弾衝突サウンドエフェクトを追加
        self.bullet_clash_sound = None
        self.bullet_clash_sound_loaded = False
        try:
            self.bullet_clash_sound = pygame.mixer.Sound(BULLET_CLASH_SOUND_PATH)
            self.bullet_clash_sound.set_volume(1.0) # サウンドの音量を100%に設定
            self.bullet_clash_sound_loaded = True
            print(f"弾衝突サウンドの読み込みに成功: {BULLET_CLASH_SOUND_PATH}")
        except pygame.error as e:
            print(f"弾衝突サウンドの読み込みに失敗: {e}")
            print(f"パス: {BULLET_CLASH_SOUND_PATH}")
            
        # 防護壁(バリア)点滅音を追加
        self.barrier_blink_sound = None
        self.barrier_blink_sound_loaded = False
        self.barrier_blink_channel = pygame.mixer.find_channel() # 専用チャンネルを取得
        if self.barrier_blink_channel is None:
            print("専用チャンネルを取得できませんでした。")
        try:
            self.barrier_blink_sound = pygame.mixer.Sound(BARRIER_BLINK_SOUND_PATH)
            self.barrier_blink_sound.set_volume(0.6) # サウンドの音量を60%に設定
            self.barrier_blink_sound_loaded = True
            print(f"防護壁サウンドの読み込みに成功: {BARRIER_BLINK_SOUND_PATH}")
        except pygame.error as e:
            print(f"防護壁サウンドの読み込みに失敗: {e}")
            print(f"パス: {BARRIER_BLINK_SOUND_PATH}")
            
        # 点滅中バリアカウンターを追加
        self.blinking_barrier_count = 0     
        # 初期状態とタイマー
        self.game_state = STATE_TITLE # 初期状態をタイトルに
        self.title_timer = 0 # タイトル表示用タイマー
        self.score = 0
        self.stage = 1
        self.stage_clear_timer = 0
        self.game_over_timer = 0
        # 通常型UFOタイマー
        self.ufo_timer = 0
        self.next_ufo_spawn_time = random.randint(UFO_SPAWN_INTERVAL_MIN, UFO_SPAWN_INTERVAL_MAX)
        # 攻撃UFOタイマー
        self.attacking_ufo_timer = 0
        self.next_attacking_ufo_spawn_time = random.randint(ATTACKING_UFO_SPAWN_INTERVAL_MIN, ATTACKING_UFO_SPAWN_INTERVAL_MAX)
        # デモプレイリセット用フラグ
        self.trigger_demo_reset = False
        # プレイヤー被弾メッセージ用メソッド
        # 表示するメッセージ
        self.player_hit_message = None
        # 表示残り時間
        self.player_hit_message_timer = 0
        # ゲームオーバーBGM再生済みフラグ
        self.gameover_bgm_played = False
        # Passive UFOタイマー
        self.passive_ufo_timer = 0
        self.next_passive_ufo_spawn_time = random.randint(PASSIVE_UFO_SPAWN_INTERVAL_MIN, PASSIVE_UFO_SPAWN_INTERVAL_MAX)
        # Random Shooter UFOタイマー
        self.random_shooter_ufo_timer = 0
        self.next_random_shooter_ufo_spawn_time = random.randint(RANDOM_SHOOTER_UFO_SPAWN_INTERVAL_MIN, RANDOM_SHOOTER_UFO_SPAWN_INTERVAL_MAX)
        
        # スプライトグループ
        self.all_sprites = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.barriers = pygame.sprite.Group()
        self.ufo_group = pygame.sprite.GroupSingle() # UFOは同時に1体まで
        # 攻撃UFO関連グループ
        self.attacking_ufo_group = pygame.sprite.GroupSingle() # 攻撃UFOも同時に1体まで
        self.attacking_ufo_bullets = pygame.sprite.Group() # 攻撃UFOの弾グループ
        self.particles = pygame.sprite.Group()
        # Passive UFO関連グループ
        self.passive_ufos = pygame.sprite.Group()
        # Random Shooter UFO関連グループ
        self.random_shooter_ufo_group = pygame.sprite.GroupSingle() # 同時に1体まで
        self.random_shooter_ufo_bullets = pygame.sprite.Group() # 専用の弾グループ

        self.particles = pygame.sprite.Group()
        self.player = None # プレイヤーオブジェクトは reset_game または reset_demo_play で作成

        # タイトルスクロール用変数
        self.title_scroll_text = [
            ("", TITLE_TEXT_COLOR, None), # 上部の余白用
            ("", TITLE_TEXT_COLOR, None),
            # ゲームタイトル
            (CAPTION, TITLE_TEXT_COLOR, TITLE_SCROLL_FONT_SIZE), 
            ("", TITLE_TEXT_COLOR, None),
            # サブタイトル
            ("A Simple Invader - like Game", TITLE_TEXT_COLOR_HIGHLIGHT, FONT_SIZE_NORMAL), # サブタイトル
            ("", TITLE_TEXT_COLOR, None),
            ("--- HOW TO PLAY ---", TITLE_TEXT_COLOR_NORMAL, FONT_SIZE_NORMAL),
            ("", TITLE_TEXT_COLOR, None),
            ("Arrow Keys: Move", TITLE_TEXT_COLOR_NORMAL, FONT_SIZE_NORMAL),
            ("Space: Shoot", TITLE_TEXT_COLOR_NORMAL, FONT_SIZE_NORMAL),
            ("ESC: Quit", TITLE_TEXT_COLOR_NORMAL, FONT_SIZE_NORMAL),
            ("", TITLE_TEXT_COLOR, None),
            ("", TITLE_TEXT_COLOR, None),
            ("--- FEATURES ---", TITLE_TEXT_COLOR_NORMAL, FONT_SIZE_NORMAL),
            ("", TITLE_TEXT_COLOR, None),
            ("Multiple Alien Types (Visual)", TITLE_TEXT_COLOR_NORMAL, FONT_SIZE_NORMAL),
            ("UFOs (Normal, Attacking, Passive, Random Shooter)", TITLE_TEXT_COLOR_NORMAL, FONT_SIZE_NORMAL),
            ("Barriers", TITLE_TEXT_COLOR_NORMAL, FONT_SIZE_NORMAL),
            ("Particle Effects", TITLE_TEXT_COLOR_NORMAL, FONT_SIZE_NORMAL),
            ("Sound Effects & BGM", TITLE_TEXT_COLOR_NORMAL, FONT_SIZE_NORMAL),
            ("Increasing Difficulty", TITLE_TEXT_COLOR_NORMAL, FONT_SIZE_NORMAL),
            ("Stage Bonuses", TITLE_TEXT_COLOR_NORMAL, FONT_SIZE_NORMAL),
            ("", TITLE_TEXT_COLOR, None),
            ("Press ENTER to Start Game", TITLE_TEXT_COLOR_HIGHLIGHT, FONT_SIZE_LARGE),
            ("", TITLE_TEXT_COLOR, None),
            ("Auto - starts Demo Play...", TITLE_TEXT_COLOR_NORMAL, FONT_SIZE_NORMAL),
            # ... さらにテキストを追加可能 ...
        ]
        
        # self.title_scroll_font = pygame.font.Font(FONT_NAME, TITLE_SCROLL_FONT_SIZE)
        # self.title_line_height = self.title_scroll_font.get_linesize() + TITLE_SCROLL_SPACING
        # self.title_text_surfaces = [] # レンダリング済みテキストSurface
        
        # デフォルトのフォントサイズと行の高さを保持
        self.default_title_font = pygame.font.Font(FONT_NAME, TITLE_SCROLL_FONT_SIZE)
        self.default_title_line_height = self.default_title_font.get_linesize() + TITLE_SCROLL_SPACING
        # レンダリング済みSurface実際の高さを格納するリスト
        self.title_rendered_lines = [] # [(surface, height),(surface, height), …]
        
        self.total_title_text_height = 0
        self.title_scroll_y = HEIGHT # 画面下端から開始
    
        # タイトルスクロール初期化
        self._initialize_title_scroll() # 初回起動時の初期化
        
    # タイトルスクロール初期化メソッド
    def _initialize_title_scroll(self):
        """
        タイトルスクロール用のテキストレンダリングと変数初期化
        """
        self.title_rendered_lines = [] # レンダリング済みSurfaceと高さを格納するリストを初期化
        self.total_title_text_height = 0 # 全体の高さを初期化
        
        for line, color, size in self.title_scroll_text:
            if line: # textのある行
                # フォントサイズを変更
                font_size = size if size is not None else TITLE_SCROLL_FONT_SIZE
                try:
                    # 指定されたサイズのフォントオブジェクトを作成
                    font = pygame.font.Font(FONT_NAME, font_size)
                    # テキストをレンダリング
                    surf = font.render(line, True, color)
                    # この行の高さを計算(フォントの高さ + 行間)
                    height = font.get_linesize() + TITLE_SCROLL_SPACING
                    # レンダリング済みSurfaceと高さをリストに追加
                    self.title_rendered_lines.append((surf, height)) # タプルとして追加
                    # 全体の高さにこの行の高さを加算
                    self.total_title_text_height += height
                except pygame.error as e:
                    # フォント作成やレンダリングエラーが発生した場合
                    print(f"Error rendering title line '{line}' with size {font_size}: {e}")
                    # エラー時はデフォルトの高さで空行として扱う
                    height = self.default_title_line_height 
                    # エラー時もプレースホルダーを追加するほうが一貫性があるかもしれない
                    self.title_rendered_lines.append((None, height))
                    self.total_title_text_height += height
            else: # 空行
                # デフォルトの高さを使用
                height = self.default_title_line_height
                # 空行の場合も(None, height)タプルを追加
                self.title_rendered_lines.append((None, height))
                # 全体の高さに加算
                self.total_title_text_height += height

        # self.total_title_text_height = len(self.title_text_surfaces) * self.title_line_height
        self.title_scroll_y = HEIGHT # スクロール位置を画面下端にリセット
        # print("Title scroll initialized.") # debug
    
    def _create_aliens(self):
        """
        エイリアンを生成
        """
        # --- デモプレイ用にステージ1相当で生成 ---
        stage_for_calc = 1 if self.game_state == STATE_DEMO_PLAY else self.stage
        alien_start_y = ALIEN_START_Y_BASE + (stage_for_calc - 1) * ALIEN_STAGE_Y_OFFSET
        current_alien_speed = ALIEN_BASE_SPEED + (stage_for_calc - 1) * 0.5
        current_alien_down_speed = ALIEN_BASE_DOWN_SPEED + (stage_for_calc - 1) * 0.5
        
        for i in range(ALIEN_ROWS):
            for j in range(ALIEN_COLS):
                x = ALIEN_START_X + j * (ALIEN_WIDTH + ALIEN_X_GAP)
                y = alien_start_y + i * (ALIEN_HEIGHT + ALIEN_Y_GAP)
                color = ALIEN_COLORS[i % len(ALIEN_COLORS)]
                score = ALIEN_SCORES[i % len(ALIEN_SCORES)]
                alien = Alien(x, y, color, score, current_alien_speed, current_alien_down_speed)
                self.all_sprites.add(alien)
                self.aliens.add(alien)

    def _create_barriers(self):
        """
        防護壁を生成
        """
        for i in range(BARRIER_COUNT):
            x = BARRIER_GAP + i * (BARRIER_WIDTH + BARRIER_GAP)
            barrier = Barrier(x, BARRIER_Y,self) # Barrier生成時に self を渡す
            self.all_sprites.add(barrier)
            self.barriers.add(barrier)

    def _create_particles(self, center, num_particles=12):
        """
        指定位置に火花パーティクルを生成
        """
        for _ in range(num_particles):
            particle = Particle(center[0], center[1])
            self.all_sprites.add(particle)
            self.particles.add(particle) # particlesグループにも追加

    def _clear_all_sprites(self):
        """
        プレイヤー以外の全てのスプライトを削除するヘルパー関数
        """
        for sprite in self.all_sprites:
            if sprite != self.player:
                sprite.kill()
        self.aliens.empty()
        self.player_bullets.empty()
        self.alien_bullets.empty()
        self.barriers.empty()
        self.ufo_group.empty()
        # 攻撃UFO関連グループのクリア
        self.attacking_ufo_group.empty()
        self.attacking_ufo_bullets.empty()
        # Passive UFO関連グループのクリア
        self.passive_ufos.empty()
        # Random Shooter UFO関連グループのクリア
        self.random_shooter_ufo_group.empty()
        self.random_shooter_ufo_bullets.empty()
        
        self.particles.empty()

    def reset_stage(self):
        """
        ステージをリセット (プレイ中用)
        """
        self._clear_all_sprites()
        self._create_aliens()
        self._create_barriers()

        # プレイヤーの位置をリセット
        if self.player:
            self.player.rect.centerx = PLAYER_START_X + PLAYER_WIDTH // 2
            self.player.rect.bottom = PLAYER_START_Y + PLAYER_HEIGHT

        self.game_state = STATE_PLAYING
        self.stage_clear_timer = 0
        # UFOタイマーリセット
        self.ufo_timer = 0
        self.next_ufo_spawn_time = random.randint(UFO_SPAWN_INTERVAL_MIN, UFO_SPAWN_INTERVAL_MAX)
        # 攻撃UFOタイマーリセットを追加
        self.attacking_ufo_timer = 0
        self.next_attacking_ufo_spawn_time = random.randint(ATTACKING_UFO_SPAWN_INTERVAL_MIN, ATTACKING_UFO_SPAWN_INTERVAL_MAX)
        # Passive UFOタイマーリセットを追加
        self.passive_ufo_timer = 0
        self.next_passive_ufo_spawn_time = random.randint(PASSIVE_UFO_SPAWN_INTERVAL_MIN, PASSIVE_UFO_SPAWN_INTERVAL_MAX)
        # Random Shooter UFOタイマーリセットを追加
        self.random_shooter_ufo_timer = 0
        self.next_random_shooter_ufo_spawn_time = random.randint(RANDOM_SHOOTER_UFO_SPAWN_INTERVAL_MIN, RANDOM_SHOOTER_UFO_SPAWN_INTERVAL_MAX)
        # バリア点滅カウンターとサウンドをリセット
        self.blinking_barrier_count = 0
        if self.barrier_blink_channel:
            self.barrier_blink_channel.stop()

    # デモプレイリセット用メソッド
    def reset_demo_play(self):
        """
        デモプレイを初期状態に戻す
        """
        #  BGM停止を追加
        if self.bgm_loaded:
            pygame.mixer.music.stop()
        # ゲームオーバーBGMも停止(念のため)
        if self.gameover_sound_loaded:
            self.gameover_sound.stop() 
        
        # 既存のスプライトをクリア
        if self.player:
            self.player.kill()
        self._clear_all_sprites()

        # デモ用プレイヤーを作成
        self.player = Player(self, is_demo=True)
        self.all_sprites.add(self.player)

        # エイリアンとバリアを生成 (ステージ1相当)
        self._create_aliens()
        self._create_barriers()

        # タイマーリセット
        self.ufo_timer = 0
        self.next_ufo_spawn_time = random.randint(UFO_SPAWN_INTERVAL_MIN, UFO_SPAWN_INTERVAL_MAX)
        # 攻撃UFOタイマーリセットを追加 
        self.attacking_ufo_timer = 0
        self.next_attacking_ufo_spawn_time = random.randint(ATTACKING_UFO_SPAWN_INTERVAL_MIN, ATTACKING_UFO_SPAWN_INTERVAL_MAX)
        # Passive UFOタイマーリセットを追加
        self.passive_ufo_timer = 0
        self.next_passive_ufo_spawn_time = random.randint(PASSIVE_UFO_SPAWN_INTERVAL_MIN, PASSIVE_UFO_SPAWN_INTERVAL_MAX)   
        # Random Shooter UFOタイマーリセットを追加
        self.random_shooter_ufo_timer = 0
        self.next_random_shooter_ufo_spawn_time = random.randint(RANDOM_SHOOTER_UFO_SPAWN_INTERVAL_MIN, RANDOM_SHOOTER_UFO_SPAWN_INTERVAL_MAX)  

        self.trigger_demo_reset = False # リセットフラグを解除
        self.game_state = STATE_DEMO_PLAY # 状態をデモプレイに設定
        # バリア点滅カウンターとサウンドをリセット
        self.blinking_barrier_count = 0
        if self.barrier_blink_channel:
            self.barrier_blink_channel.stop()
        print("Demo play reset.")

    def reset_game(self):
        """
        ゲーム全体を初期状態に戻す (新規ゲーム開始用)
        """
        self.score = 0
        self.stage = 1
        
        # ゲームオーバーBGM停止を追加
        if self.gameover_sound_loaded:
            self.gameover_sound.stop()

        # 既存のスプライトをクリア
        if self.player:
            self.player.kill()
        self._clear_all_sprites()

        # 新しいプレイヤーを作成 (通常プレイヤー)
        self.player = Player(self, is_demo=False)
        self.all_sprites.add(self.player)

        # ステージ1をセットアップ
        self.reset_stage() # reset_stage が game_state を PLAYING に設定する

        # BGM再生開始を追加
        if self.bgm_loaded:
            pygame.mixer.music.play(loops=-1) # loops=-1で無限ループ再生
            
        # Passive UFOタイマーリセットは reset_stage で行われるので不要かと…
        # self.passive_ufo_timer = 0
        # self.next_passive_ufo_spawn_time = random.randint(PASSIVE_UFO_SPAWN_INTERVAL_MIN, PASSIVE_UFO_SPAWN_INTERVAL_MAX)
    
    def _update_random_shooter_ufo(self):
        """
        Random Shooter UFOの出現ロジック
        """
        if not self.random_shooter_ufo_group: # UFOがいない場合
            self.random_shooter_ufo_timer += 1
            if self.random_shooter_ufo_timer >= self.next_random_shooter_ufo_spawn_time:
                random_shooter_ufo = RandomShooterUFO(self) # Gameオブジェクトを渡す
                if random_shooter_ufo.image: # 画像が正常に読み込めた場合のみ追加
                    self.all_sprites.add(random_shooter_ufo)
                    self.random_shooter_ufo_group.add(random_shooter_ufo)
                self.random_shooter_ufo_timer = 0
                self.next_random_shooter_ufo_spawn_time = random.randint(RANDOM_SHOOTER_UFO_SPAWN_INTERVAL_MIN, RANDOM_SHOOTER_UFO_SPAWN_INTERVAL_MAX)    
        
    def handle_events(self):
        """
        イベント処理
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # ESCキーで終了
                    self.running = False

                # --- 状態に応じたEnterキー処理 ---
                if self.game_state == STATE_TITLE and event.key == pygame.K_RETURN:
                    # スクロールを中断してゲーム開始
                    print("Enter Pressed in Title. Starting Game…")
                    # BGMやサウンドを停止(念のため)
                    if self.bgm_loaded:
                        pygame.mixer.music.stop()
                    if self.gameover_sound_loaded:
                        self.gameover_sound.stop()
                    if self.barrier_blink_channel:
                        self.barrier_blink_channel.stop()
                    self.blinking_barrier_count = 0    
                    self.reset_game() # タイトル画面からゲーム開始
                elif self.game_state == STATE_DEMO_PLAY and event.key == pygame.K_RETURN:
                    self.reset_game() # デモプレイ画面からゲーム開始

                # プレイ中にスペースキーで弾発射
                elif self.game_state == STATE_PLAYING and event.key == pygame.K_SPACE:
                    if self.player and not self.player.is_demo: # 通常プレイヤーのみ
                        self.player.shoot()

    def _update_aliens(self):
        """
        エイリアンの移動と発射ロジック
        """
        move_down = False
        # 左右端チェック
        for alien in self.aliens:
            if alien.rect.left <= 0 or alien.rect.right >= WIDTH:
                move_down = True
                break # 一体でも端に到達したら下に移動

        # 下移動と方向転換
        if move_down:
            for alien in self.aliens:
                alien.reverse_direction()
                alien.update(move_down=True) # 下移動フラグを渡す
        else:
            # 通常の横移動のみ (Alien.update() は all_sprites.update() で呼ばれる)
            pass # ここでの呼び出しは不要

        # エイリアンの発射
        bottom_aliens_in_col = {}
        for alien in self.aliens:
            # 列インデックスの計算
            col_index = (alien.rect.centerx - ALIEN_START_X) // (ALIEN_WIDTH + ALIEN_X_GAP)
            if col_index not in bottom_aliens_in_col or alien.rect.bottom > bottom_aliens_in_col[col_index].rect.bottom:
                bottom_aliens_in_col[col_index] = alien

        # 発射判定
        if bottom_aliens_in_col:
            fire_rate_adjust = max(1, len(bottom_aliens_in_col))
            # --- デモプレイ用にステージ1相当で計算 ---
            stage_for_calc = 1 if self.game_state == STATE_DEMO_PLAY else self.stage
            num_aliens_total = ALIEN_ROWS * ALIEN_COLS
            num_aliens_current = len(self.aliens)
            # エイリアン減少によるレート上昇 (デモでも適用)
            fire_rate_multiplier = 1 + (num_aliens_total - num_aliens_current) * 0.02 # 係数を調整
            # ステージによるレート上昇 (プレイ中のみ)
            # if self.game_state == STATE_PLAYING:
            fire_rate_multiplier *= (1 + (stage_for_calc - 1) * 0.1) # ステージが進むと少し速くなる

            current_fire_rate = ALIEN_FIRE_RATE_BASE / fire_rate_multiplier
            fire_chance = max(1, int(current_fire_rate / fire_rate_adjust))

            for alien in bottom_aliens_in_col.values():
                if random.randint(0, fire_chance) == 0:
                    # Bulletに is_wave 引数を追加
                    bullet = Bullet(alien.rect.centerx, alien.rect.bottom, ALIEN_BULLET_SPEED, RED, is_wave=True)
                    self.all_sprites.add(bullet)
                    self.alien_bullets.add(bullet)

    def _update_ufo(self):
        """
        通常型UFOの出現・移動ロジック
        """
        if not self.ufo_group: # UFOがいない場合
            self.ufo_timer += 1
            if self.ufo_timer >= self.next_ufo_spawn_time:
                ufo = UFO()
                if ufo.image: # 画像が正常に読み込めた場合のみ追加
                    self.all_sprites.add(ufo)
                    self.ufo_group.add(ufo)
                self.ufo_timer = 0
                self.next_ufo_spawn_time = random.randint(UFO_SPAWN_INTERVAL_MIN, UFO_SPAWN_INTERVAL_MAX)
        # else: # UFO の update は all_sprites.update() で呼ばれる
        #     self.ufo_group.update()
    
    # 攻撃UFOの出現ロジック
    def _update_attacking_ufo(self):
        """
        攻撃UFOの出現ロジック
        """
        if not self.attacking_ufo_group: # 攻撃UFOがいない場合
            self.attacking_ufo_timer += 1
            if self.attacking_ufo_timer >= self.next_attacking_ufo_spawn_time:
                attacking_ufo = AttackingUFO(self) # Gameオブジェクトを渡す
                if attacking_ufo.image: # 画像が正常に読み込めた場合のみ追加
                    self.all_sprites.add(attacking_ufo)
                    self.attacking_ufo_group.add(attacking_ufo)
                self.attacking_ufo_timer = 0
                self.next_attacking_ufo_spawn_time = random.randint(ATTACKING_UFO_SPAWN_INTERVAL_MIN, ATTACKING_UFO_SPAWN_INTERVAL_MAX)
        # else: # AttackingUFO の update は all_sprites.update() で呼ばれる
    
    # Passive UFOの出現ロジック
    def _update_passive_ufo(self):
        """
        Passive UFOの出現ロジック
        """
        # 画面上の数が最大未満の場合のみタイマーを進める
        if len(self.passive_ufos) < PASSIVE_UFO_MAX_COUNT:
            self.passive_ufo_timer += 1
            if self.passive_ufo_timer >= self.next_passive_ufo_spawn_time:
                passive_ufo = PassiveUFO()
                if passive_ufo.image: # 画像が正常に読み込めた場合のみ追加
                    self.all_sprites.add(passive_ufo)
                    self.passive_ufos.add(passive_ufo)
                self.passive_ufo_timer = 0
                self.next_passive_ufo_spawn_time = random.randint(PASSIVE_UFO_SPAWN_INTERVAL_MIN, PASSIVE_UFO_SPAWN_INTERVAL_MAX)
        # PassiveUFO の update は all_sprites.update() で呼ばれる
    
    def _check_collisions(self):
        """
        衝突判定
        """
        # プレイヤー弾 vs エイリアン
        hits = pygame.sprite.groupcollide(self.aliens, self.player_bullets, True, True)        
        for alien in hits:
            # --- デモ中はスコア加算しない ---
            if self.game_state == STATE_PLAYING:
                self.score += alien.score

            self._create_particles(alien.rect.center)

        # エイリアン弾 vs プレイヤー
        if self.player and self.player.alive(): # プレイヤー存在チェック
            collided_alien_bullets = pygame.sprite.spritecollide(self.player, self.alien_bullets, True)
            if collided_alien_bullets:
                self.player.hit() # hitメソッド内でデモか通常か判定
                self._create_particles(self.player.rect.center)
        
         # 攻撃UFO弾 vs プレイヤー 
        if self.player and self.player.alive():
            collided_attacking_ufo_bullets = pygame.sprite.spritecollide(self.player, self.attacking_ufo_bullets, True)
            if collided_attacking_ufo_bullets:
                self.player.hit() # 同じく hit メソッドを呼ぶ
                self._create_particles(self.player.rect.center, num_particles=5) # 少し違うエフェクトにしても良い

        # Random Shooter UFO vs プレイヤー
        if self.player and self.player.alive():
            collided_random_shooter_ufo_bullets = pygame.sprite.spritecollide(self.player, self.random_shooter_ufo_bullets, True)
            if collided_random_shooter_ufo_bullets:
                self.player.hit() # 同じく hit メソッドを呼ぶ
                self._create_particles(self.player.rect.center, num_particles=5) # 少し違うエフェクトにしても良い
                
        # プレイヤー弾 vs 防護壁
        bullets_hit_barrier = pygame.sprite.groupcollide(self.barriers, self.player_bullets, False, True)
        for barrier, bullets in bullets_hit_barrier.items():
            barrier.hit(len(bullets))
            for bullet in bullets:
                 if barrier.alive(): # バリアがまだ存在する場合のみ
                    self._create_particles(bullet.rect.center, num_particles=3)

        # エイリアン弾 vs 防護壁
        alien_bullets_hit_barrier = pygame.sprite.groupcollide(self.barriers, self.alien_bullets, False, True)
        for barrier, bullets in alien_bullets_hit_barrier.items():
            barrier.hit(len(bullets))
            for bullet in bullets:
                 if barrier.alive(): # バリアがまだ存在する場合のみ
                    self._create_particles(bullet.rect.center, num_particles=3)

        # 攻撃UFO弾 vs 防護壁
        attacking_ufo_bullets_hit_barrier = pygame.sprite.groupcollide(self.barriers, self.attacking_ufo_bullets, False, True)
        for barrier, bullets in attacking_ufo_bullets_hit_barrier.items():
            barrier.hit(len(bullets)) # 同じく hit メソッドを呼ぶ
            for bullet in bullets:
                 if barrier.alive():
                    self._create_particles(bullet.rect.center, num_particles=2) # 少し違うエフェクトにしても良い
    
        # Random Shooter UFO弾 vs 防護壁
        random_shooter_ufo_bullets_hit_barrier = pygame.sprite.groupcollide(self.barriers, self.random_shooter_ufo_bullets, False, True)
        for barrier, bullets in random_shooter_ufo_bullets_hit_barrier.items():
            barrier.hit(len(bullets)) # 同じく hit メソッドを呼ぶ
            for bullet in bullets:
                 if barrier.alive():
                    self._create_particles(bullet.rect.center, num_particles=3) # 少し違うエフェクトにしても良い
                    
        # プレイヤー弾 vs UFO
        if self.ufo_group.sprite:
            ufo_hit = pygame.sprite.spritecollide(self.ufo_group.sprite, self.player_bullets, True)
            if ufo_hit:
                # UFO爆発のエフェクトを追加
                if self.ufo_explosion_sound_loaded:
                    self.ufo_explosion_sound.play()
                
                if self.game_state == STATE_PLAYING:
                    self.score += UFO_SCORE

                self._create_particles(self.ufo_group.sprite.rect.center, num_particles=25)
                self.ufo_group.sprite.kill()
        
        # プレイヤー弾 vs 攻撃UFO
        if self.attacking_ufo_group.sprite:
            attacking_ufo_hit = pygame.sprite.spritecollide(self.attacking_ufo_group.sprite, self.player_bullets, True)
            if attacking_ufo_hit:
                # UFO爆発のエフェクトを追加
                if self.ufo_explosion_sound_loaded:
                    self.ufo_explosion_sound.play()    
                
                if self.game_state == STATE_PLAYING:
                    self.score += ATTACKING_UFO_SCORE # 攻撃UFOのスコアを加算

                self._create_particles(self.attacking_ufo_group.sprite.rect.center, num_particles=30) # 少し派手なエフェクト
                self.attacking_ufo_group.sprite.kill()

        # プレイヤー弾 vs Random Shooter UFO
        if self.random_shooter_ufo_group.sprite:
            random_shooter_ufo_hit = pygame.sprite.spritecollide(self.random_shooter_ufo_group.sprite, self.player_bullets, True)
            if random_shooter_ufo_hit:
                # UFO爆発のエフェクトを追加
                if self.ufo_explosion_sound_loaded:
                    self.ufo_explosion_sound.play()    
                
                if self.game_state == STATE_PLAYING:
                    self.score += RANDOM_SHOOTER_UFO_SCORE # Random Shooter UFOのスコアを加算

                self._create_particles(self.random_shooter_ufo_group.sprite.rect.center, num_particles=45) # 少し派手なエフェクト
                self.random_shooter_ufo_group.sprite.kill()

        # エイリアン vs 防護壁
        aliens_touching_barrier = pygame.sprite.groupcollide(self.barriers, self.aliens, False, False)
        for barrier, aliens in aliens_touching_barrier.items():
            if barrier.alive():
                self._create_particles(barrier.rect.center, num_particles=15)
                barrier.alien_touch()

        # 弾同士の衝突 (エイリアン弾 vs プレイヤー弾)
        bullet_collisions = pygame.sprite.groupcollide(self.player_bullets, self.alien_bullets, True, True)
        if bullet_collisions: # 衝突があった場合のみサウンドエフェクト再生
            if self.bullet_clash_sound_loaded:
                self.bullet_clash_sound.play()
        for player_bullet, alien_bullets_list in bullet_collisions.items():
            explosion_pos = player_bullet.rect.center
            self._create_particles(explosion_pos, num_particles=5)
            # スコア加算処理
            if self.game_state == STATE_PLAYING:
                # 衝突したエイリアン弾1つに対してスコア加算
                score_per_collision = 250 # 衝突時のスコア
                # len()で参照
                self.score += len(alien_bullets_list) * score_per_collision
                # print(f"Bullet cllision! Score + {len(alien_bullets_list) * score_per_collision}") # デバッグ用

        # 弾同士の衝突 (プレイヤー弾 vs 攻撃型UFO弾)
        player_vs_attacking_ufo_bullets = pygame.sprite.groupcollide(self.player_bullets, self.attacking_ufo_bullets, True, True)
        if player_vs_attacking_ufo_bullets: # 衝突があった場合のみサウンドエフェクト再生
            if self.bullet_clash_sound_loaded:
                self.bullet_clash_sound.play()
        for player_bullet, attacking_ufo_bullets_list in player_vs_attacking_ufo_bullets.items():
            explosion_pos = player_bullet.rect.center
            self._create_particles(explosion_pos, num_particles=7) # 少し違うエフェクト
            if self.game_state == STATE_PLAYING:
                score_per_collision = 500 # 攻撃UFO弾との衝突スコア
                self.score += len(attacking_ufo_bullets_list) * score_per_collision

        # 弾同士の衝突 (プレイヤー弾 vs Random Shooter UFO弾)
        player_vs_random_shooter_ufo_bullets = pygame.sprite.groupcollide(self.player_bullets, self.random_shooter_ufo_bullets, True, True)
        if player_vs_random_shooter_ufo_bullets: # 衝突があった場合のみサウンドエフェクト再生
            if self.bullet_clash_sound_loaded:
                self.bullet_clash_sound.play()
        for player_bullet, random_shooter_ufo_bullets_list in player_vs_random_shooter_ufo_bullets.items():
            explosion_pos = player_bullet.rect.center
            self._create_particles(explosion_pos, num_particles=7) # 少し違うエフェクト
            if self.game_state == STATE_PLAYING:
                score_per_collision = 500 # Random Shooter UFO弾との衝突スコア
                self.score += len(random_shooter_ufo_bullets_list) * score_per_collision   
                
    def _check_game_over_conditions(self):
        """
        ゲームオーバー条件のチェック (プレイ中用)
        """
        if self.game_state != STATE_PLAYING: 
            return # プレイ中以外はチェックしない

        game_over_flag = False
        # エイリアンが最下部に到達
        for alien in self.aliens:
            if alien.rect.bottom >= PLAYER_START_Y: # プレイヤーの初期Y座標まで来たら
                game_over_flag = True
                print ("Game Over: Aliens reached the bottom") # デバッグ用
                break
            
        # プレイヤーライフが0
        # playerオブジェクトが存在するかチェック
        # if not game_over_flag and self.player.lives <= 0:
        if not game_over_flag and self.player and self.player.lives <= 0:
            game_over_flag = True
            print ("Game Over: Player lives reached 0") # デバッグ用
        
        if game_over_flag: # ゲームオーバー確定時にメインBGM停止
            if self.bgm_loaded:
                print("Stopping main BGM...") # デバッグ用
                pygame.mixer.music.stop()
            self.game_state = STATE_GAME_OVER
            self.game_over_timer = 0 # タイマーリセット
            self.gameover_bgm_played = False # ゲームオーバーBGM再生フラグをリセット  
            if self.player and self.player.alive():
                self._create_particles(self.player.rect.center, num_particles=30)
                self.player.kill()
            print(f"Game state Chenged to: {self.game_state}") # デバッグ用

    def _check_demo_over_conditions(self):
        """
        デモプレイの終了・リセット条件をチェック
        """
        if self.game_state != STATE_DEMO_PLAY: return

        # デモプレイヤーがヒットされたか (Player.hit() でフラグが立つ)
        if self.trigger_demo_reset:
            self.reset_demo_play()
            return

        # エイリアンが侵略したか
        for alien in self.aliens:
            if alien.rect.bottom >= PLAYER_START_Y:
                print("Demo: Alien reached bottom.")
                self.reset_demo_play()
                return

        # エイリアンを全滅させたか
        if not self.aliens:
            print("Demo: All aliens destroyed.")
            self.reset_demo_play()
            return

    def _check_stage_clear(self):
        """
        ステージクリア条件のチェック (プレイ中用)
        """
        if self.game_state != STATE_PLAYING:
            return # プレイ中以外はチェックしない

        if not self.aliens:
            self.game_state = STATE_STAGE_CLEAR
            self.stage_clear_timer = 0

            # 奇数ステージクリアボーナス
            if self.stage % 2 != 0:
                if self.player and self.player.lives < PLAYER_MAX_LIVES:
                    self.player.lives += 1
                    print(f"Stage {self.stage} clear! Extra life awarded. Lives: {self.player.lives}")
                else:
                    print(f"Stage {self.stage} clear! Max lives reached.")

            # 偶数ステージクリアボーナス
            if self.stage % 2 == 0:
                 self.score += 100 * self.stage
                 print(f"Stage {self.stage} clear! Score Bonus awarded: +{100 * self.stage}")

    # タイトル画面更新メソッド
    # def _update_title(self):
    #     """
    #     タイトル画面の更新処理 (タイマーと遷移)
    #     """
    #     self.title_timer += 1
    #     if self.title_timer >= TITLE_DURATION:
    #         self.title_timer = 0 # タイマーリセット
    #          # デモ開始前にBGM停止を追加（念のため)
    #         if self.bgm_loaded:
    #             pygame.mixer.music.stop()
    #         # タイトル => デモプレイ遷移時にバリア音停止(念のため)
    #         if self.barrier_blink_channel:
    #             self.barrier_blink_channel.stop()
    #         self.brinking_barrier_count = 0
    #         self.reset_demo_play() # デモプレイを開始
    
    # タイトル画面更新メソッド
    def _update_title(self):
        """
        タイトル画面の更新処理 (スクロール)
        """
        # スクロール位置を更新 (下から上へ)
        self.title_scroll_y -= TITLE_SCROLL_SPEED
        # print(f"Updating title scroll. y={self.title_scroll_y}") # debug
        print(f"Updating title scroll. y={self.title_scroll_y:.1f}, Bottom edge: {self.title_scroll_y + self.total_title_text_height:.1f}")
        
        # スクロールが完全に画面外に出たらデモプレイへ移行
        if self.title_scroll_y < -self.total_title_text_height < 0:
            print("Title scroll finished. (y={self.title_scroll_y}:.lf}<{-self.total_title_text_height}).Resetting to demo play…")
             # デモ開始前にBGM停止を追加（念のため)
            if self.bgm_loaded:
                pygame.mixer.music.stop()
            # タイトル => デモプレイ遷移時にバリア音停止(念のため)
            if self.barrier_blink_channel:
                self.barrier_blink_channel.stop()
                self.blinking_barrier_count = 0

            self.reset_demo_play() # デモプレイを開始

    # デモプレイ更新メソッド
    def _update_demo_play(self):
        """
        デモプレイ中の更新処理
        """
        # スプライト更新 (Player含む)
        self.all_sprites.update()
        # エイリアン移動・発射
        self._update_aliens()
        # UFO出現・移動
        self._update_ufo()
        # 攻撃UFO出現・移動
        self._update_attacking_ufo()
        # 衝突判定
        self._check_collisions()
        # デモプレイ終了条件チェック
        self._check_demo_over_conditions()

    def update(self):
        """
        ゲーム状態の更新
        """
        # --- ↓↓↓ 状態に応じた更新処理呼び出し ↓↓↓ ---
        if self.game_state == STATE_TITLE:
            self._update_title()
        elif self.game_state == STATE_DEMO_PLAY:
            self._update_demo_play() # _update_demo_play 内で各種updateを呼び出す
            self._update_passive_ufo() # Passive UFOのupdate
            self._update_random_shooter_ufo() # Random Shooter UFOのupdate
        elif self.game_state == STATE_PLAYING:
            # スプライト更新 (Player含む)
            self.all_sprites.update()
            # エイリアン移動・発射
            self._update_aliens()
            # UFO出現・移動
            self._update_ufo()
            # 攻撃UFO出現・移動
            self._update_attacking_ufo()
            # Passive UFO出現・移動
            self._update_passive_ufo()
            # Random Shooter UFO出現・移動
            self._update_random_shooter_ufo()
            # 衝突判定
            self._check_collisions()
            # ゲームオーバー条件チェック
            self._check_game_over_conditions()
            if self.game_state == STATE_PLAYING: # プレイ中のみチェック
                # ステージクリア条件チェック
                self._check_stage_clear()
            # プレイヤー被弾メッセージ更新
            if self.player_hit_message_timer > 0:
                self.player_hit_message_timer -= 1
                if self.player_hit_message_timer == 0:
                    self.player_hit_message = None # メッセージクリア
                                        
        elif self.game_state == STATE_STAGE_CLEAR:
            # ステージクリア中もパーティクルなどは更新
            self.all_sprites.update()
            self.stage_clear_timer += 1
            if self.stage_clear_timer >= STAGE_CLEAR_DURATION:
                self.stage += 1
                self.reset_stage() # 次のステージへ
        elif self.game_state == STATE_GAME_OVER:
            # ゲームオーバーBGM再生処理
            if self.gameover_sound_loaded and not self.gameover_bgm_played:
                self.gameover_sound.play()
                self.gameover_bgm_played = True
                
            # ゲームオーバー時のエフェクト更新
            self.all_sprites.update()
            self.game_over_timer += 1
            if self.game_over_timer >= GAME_OVER_DURATION:
                # タイトルに戻る前にBGM停止を追加
                if self.gameover_sound_loaded:
                    self.gameover_sound.stop()
                # ゲームオーバー => タイトル遷移時にバリア音停止(念のため)
                if self.barrier_blink_channel:
                    self.barrier_blink_channel.stop()
                self.binking_barrier_count = 0
                
                self.game_state = STATE_TITLE # ゲームオーバー後はタイトルへ
                # self.game_over_timer = 0 # タイマーはSTATE_GAME_OVERに入るときにリセット済み
                self._initialize_title_scroll() # タイトルスクロールを初期化
                # タイトルに戻る前にメッセージクリア
                self.player_hit_message = None
                self.player_hit_message_timer = 0
    
    # バリア点滅カウンター操作メソッドを追加
    def increment_blinking_barrier(self):
        """
        点滅を開始したバリアがあった場合に呼ばれ
        カウンターを増やし必要ならループサウンドを再生
        """
        if self.blinking_barrier_count == 0:
            # 最初の点滅バリアが出現したときだけループ再生開始
            if self.barrier_blink_sound_loaded and self.barrier_blink_channel:
                self.barrier_blink_channel.play(self.barrier_blink_sound, loops=-1)
        self.blinking_barrier_count += 1 # カウンターを増やす
            # print(f"Blinking barriers: {self.blinking_barrier_count}") # デバッグ用
    
    def decrement_blinking_barrier(self): # メソッドを追加
        """
        点滅が終了または破壊されたバリアがあった場合に呼ばれ、
        カウンターを減らし、必要ならループサウンドを停止

        カウンターを減らすことで、
        ループサウンドが停止する状況を検出する
        """
        if self.blinking_barrier_count > 0:
            self.blinking_barrier_count -= 1
            if self.blinking_barrier_count == 0:
                # 点滅していて、ループサウンドを再生中の場合
                # ループサウンドを停止する
                if self.barrier_blink_channel:
                    self.barrier_blink_channel.stop()
            # print(f"Blinking barriers: {self.blinking_barrier_count}") # デバッグ用
        # else:
            # print("Warning: decrement_blinking_barrier called when count is already 0.") # デバッグ用   

    def _draw_title(self):
        # """
        # タイトル画面を描画
        # """
        # self.screen.fill(BLACK)
        # self.draw_text(CAPTION, self.font_title, GREEN, WIDTH // 2, HEIGHT // 4, align="center")
        # self.draw_text("Press ENTER to Start", self.font_normal, CYAN, WIDTH // 2, HEIGHT // 2, align="center")
        # self.draw_text("Arrow Keys: Move", self.font_normal, GRAY, WIDTH // 2, HEIGHT * 3 // 4 - 20, align="center")
        # self.draw_text("Space: Shoot", self.font_normal, GRAY, WIDTH // 2, HEIGHT * 3 // 4 + 20, align="center")
        # self.draw_text("ESC: Quit", self.font_normal, GRAY, WIDTH // 2, HEIGHT * 3 // 4 + 60, align="center")

        """
        タイトル画面を描画 (スクロール表示、フォントサイズ対応)
        """
        # self.screen.fill(BLACK) # 背景クリアは draw メソッド側で行う

        # 表示領域 (画面全体)
        visible_area = self.screen.get_rect()
        # 現在の描画開始Y座標をスクロール位置で初期化
        current_y = self.title_scroll_y

        # debug
        # print(f"Drawing title scroll. current_y_start={self.currrent_y}, total_height={self.total_title_text_height}")
        
        for i, (text_surface, line_height) in enumerate(self.title_rendered_lines):
            # debug
            # print(f"line {i}: current_y={current_y}, line_height={self.title_line_height}")

            # 行が画面内に表示される可能性があるかチェック
            # 条件: 行上端current_yが画面下端より上 かつ 行の下端(current_y + line_height)が画面上端より下
            if current_y < visible_area.bottom and current_y + line_height > visible_area.top:
                # レンダリングされたSurfaceが存在する場合(空行ではない)
                if text_surface is not None:
                    # テキストを中央揃えで配置するためのRectを作成    
                    text_rect = text_surface.get_rect(centerx=visible_area.centerx, top=int(current_y))
                    # 仮面にテキストを描画
                    self.screen.blit(text_surface, text_rect)
                    # debug
                    # print(f" -> Blitting line{i}")
                # else: # (空行の場合)
                    # print(f" -> Skipping empty Line {i}") 
            # else: # (画面外の場合)
                # print(f" -> Line {i} is off-screen")
                
                pass

            # 次行の描画開始Y座標を更新        
            current_y += line_height
            
    def draw_text(self, text, font, color, x, y, align="topleft"):
        """
        テキスト描画ヘルパー
        """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "topleft":
            text_rect.topleft = (x, y)
        elif align == "topright":
            text_rect.topright = (x, y)
        elif align == "center":
            text_rect.center = (x, y)
        elif align == "midtop":
            text_rect.midtop = (x, y)
        elif align == "midbottom": # midbottom を追加 (必要なら)
             text_rect.midbottom = (x, y)

        self.screen.blit(text_surface, text_rect)

    def draw(self):
        """
        画面描画
        """
        # 画面のクリア方法によって変更
        # self.screen.fill(BLACK) # デフォルト背景

        # 状態に応じた描画処理呼び出し
        if self.game_state == STATE_TITLE:
            self.screen.fill(BLACK)
            self._draw_title()
        # デモプレイ時も背景画像を描画する    
        elif self.game_state == STATE_DEMO_PLAY:
            if self.background_image:
                self.screen.blit(self.background_image, (0, 0))
            else:
                self.screen.fill(BLACK)
            self._draw_demo_play() # スプライトやテキストを描画
        elif self.game_state == STATE_PLAYING or self.game_state == STATE_STAGE_CLEAR:
            # プレイ中・ステージクリア中の描画
            if self.background_image:
                self.screen.blit(self.background_image, (0, 0))
            else:
                self.screen.fill(BLACK) # 背景がなければデフォルト
                
            # プレイ中・ステージクリア中の描画(スプライトとUI)
            self.all_sprites.draw(self.screen)
            # UI要素
            self.draw_text(f"Score: {self.score}", self.font_normal, WHITE, 10, 10, align="topleft")
            self.draw_text(f"Stage: {self.stage}", self.font_normal, WHITE, WIDTH // 2, 10, align="midtop")
            if self.player and self.player.alive():
                self.draw_text(f"Lives: {self.player.lives}", self.font_normal, WHITE, WIDTH - 10, 10, align="topright")

            # プレイヤー被弾メッセージ描画
            if self.game_state == STATE_PLAYING and self.player_hit_message_timer > 0 and self.player_hit_message:
                self.draw_text(self.player_hit_message, self.font_large, YELLOW, WIDTH // 2, HEIGHT // 2, align="center")

            # ステージクリアメッセージ
            if self.game_state == STATE_STAGE_CLEAR:
                clear_text = f"Stage {self.stage} Clear!"
                life_bonus_text = ""
                score_bonus_text = ""
                if self.stage % 2 != 0:
                    if self.player and self.player.lives < PLAYER_MAX_LIVES: life_bonus_text = "Extra Life!"
                    else: life_bonus_text = "Max Lives!"
                if self.stage % 2 == 0: score_bonus_text = f"Bonus: +{100 * self.stage}"

                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                self.screen.blit(overlay, (0, 0))
                text_y = HEIGHT // 2 - 60
                self.draw_text(clear_text, self.font_large, GREEN, WIDTH // 2, text_y, align="center")
                current_y = text_y + 60
                if life_bonus_text:
                    self.draw_text(life_bonus_text, self.font_normal, CYAN, WIDTH // 2, current_y, align="center")
                    current_y += 60
                if score_bonus_text:
                    self.draw_text(score_bonus_text, self.font_normal, YELLOW, WIDTH // 2, current_y, align="center")

        elif self.game_state == STATE_GAME_OVER:
            # ゲームオーバー画面の描画
            # ゲームオーバー時も背景画像を使う場合
            if self.background_image:
                self.screen.blit(self.background_image, (0, 0))
            else:
                self.screen.fill(BLACK) # 背景がなければデフォルト
                
            self.all_sprites.draw(self.screen) # エフェクトは表示
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            self.draw_text("Game Over", self.font_large, RED, WIDTH // 2, HEIGHT // 2 - 40, align="center")
            self.draw_text(f"Final Score: {self.score}", self.font_normal, WHITE, WIDTH // 2, HEIGHT // 2 + 20, align="center")
            self.draw_text("Returning to Title...", self.font_normal, GRAY, WIDTH // 2, HEIGHT - 50, align="center")

        pygame.display.flip()
        
    # デモプレイ画面描画メソッド
    def _draw_demo_play(self):
        """
        デモプレイ画面を描画
        """
        # self.screen.fill(BLACK) # ← drawメソッド側で背景処理をするので、ここは不要
        
        # 全てのスプライトを描画
        self.all_sprites.draw(self.screen)
        # デモプレイ中であることを示すテキスト
        self.draw_text("DEMO PLAY", self.font_normal, YELLOW, WIDTH // 2, 10, align="midtop")
        self.draw_text("Press ENTER to Start", self.font_normal, YELLOW, WIDTH // 2, HEIGHT - 40, align="center")

    def run(self):
        """
        メインゲームループ
        """
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

# --- ゲーム実行 ---
if __name__ == '__main__':
    game = Game()
    game.run()
