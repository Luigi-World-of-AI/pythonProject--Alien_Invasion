import pygame
from pygame.sprite import Group
from pygame import mixer

from settings import Settings
from space_ship import Ship
import game_functions as gf
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


# variavel global do event.scancode para capturar keypress
actual_scan = ''


def run_game():
    # define variável global no escopo(função)
    global actual_scan

    # inicia pygame, configurações e janela
    pygame.init()
    settings = Settings(None)
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    stats = GameStats(settings)
    sb = Scoreboard(settings, screen, stats)

    # cria instâncias principais
    ship = Ship(settings, screen, None)
    alien = Alien(settings, screen)
    bullets = Group()
    explosion_sprites = Group()
    explosion_rock = Group()
    alien_sprites = Group()
    rock_sprites = Group()
    play_button = Button(settings, screen, 'Play')

    # background sound
    # Instantiate mixer
    mixer.init()
    # Load audio file
    mixer.music.load('images/background.mp3')
    # Set preferred volume
    mixer.music.set_volume(0.2)

    while True:

        # responde ao evento
        # atualiza event.scancode somente quando check_events retorna algo
        scancode = gf.check_events(settings, screen, ship,
                                   bullets, stats, play_button, sb)

        if scancode is not None:
            actual_scan = scancode

        if stats.game_active:
            if settings.pause:
                text_update = gf.UpdateText(screen, actual_scan)

                # atualiza movimento da nave
                ship.update_movement()

                # atualiza movimento dos aliens
                gf.alien_update(settings, screen, alien_sprites, bullets)

                # atualiza movimento dos asteroids
                gf.rock_update(settings, screen, rock_sprites, bullets)

                # atualiza colisoes entre nave e aliens
                gf.update_ship_alien_explosions(settings, screen,
                                                ship, text_update,
                                                bullets, explosion_sprites,
                                                alien_sprites, stats, play_button,
                                                sb, rock_sprites, explosion_rock)

                # atualiza colisoes entre nave e asteroids
                gf.update_ship_rock_explosions(settings, screen, ship, text_update,
                                               bullets, explosion_sprites, alien_sprites,
                                               stats, play_button, sb, rock_sprites, explosion_rock)

                # atualiza tiros
                gf.update_bullets(settings, screen, bullets,
                                  alien_sprites, explosion_sprites, stats,
                                  sb, rock_sprites, explosion_rock)

                # atualiza tela
                gf.update_screen(settings, screen, ship,
                                 text_update, bullets, explosion_sprites,
                                 alien_sprites, play_button, stats,
                                 sb, rock_sprites, explosion_rock)

        else:
            play_button.draw_button()
            text_update = gf.UpdateText(screen, actual_scan)
            gf.update_screen(settings, screen, ship,
                             text_update, bullets, explosion_sprites,
                             alien_sprites, play_button, stats,
                             sb, rock_sprites, explosion_rock)

            # Play the music
            mixer.music.play()


run_game()
