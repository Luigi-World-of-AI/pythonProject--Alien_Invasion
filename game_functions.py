import sys
from time import sleep
import pygame
from pygame import mixer

import alien
import rock
from settings import Settings, Explosion
from bullet import Bullet


class UpdateText(Settings):
    def __init__(self, screen, key_cap):
        # define texto configurado em settings
        super().__init__(key_cap)
        self.screen = screen
        self.text_rect = self.text.get_rect()

    def blitme(self):
        self.screen.blit(self.text, self.text_rect)


def check_key_up(event, ship):
    if event.key == pygame.K_UP:
        ship.move_up = False
    elif event.key == pygame.K_DOWN:
        ship.move_down = False
    elif event.key == pygame.K_RIGHT:
        ship.move_right = False
    elif event.key == pygame.K_LEFT:
        ship.move_left = False


def check_key_down(event, settings, screen, ship, bullets):
    if event.key == pygame.K_UP:
        ship.move_up = True

    elif event.key == pygame.K_DOWN:
        ship.move_down = True

    elif event.key == pygame.K_RIGHT:
        ship.move_right = True

    elif event.key == pygame.K_LEFT:
        ship.move_left = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)

    elif event.key == pygame.K_ESCAPE:
        settings.pause = not settings.pause


def check_events(settings, screen, ship, bullets, stats, play_button, sb):
    """Respond to keypresses and mouse events."""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_key_down(event, settings, screen, ship, bullets)
            # return the scancode of key
            scancode = event.scancode
            return scancode

        elif event.type == pygame.KEYUP:
            check_key_up(event, ship)
            # return the scancode of key
            scancode = event.scancode
            return scancode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, ship, settings, sb)


def check_play_button(stats, play_button, mouse_x, mouse_y, ship, settings, sb):
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        stats.game_active = True
        stats.reset_stats()
        pygame.mouse.set_visible(False)
        ship.rect.center = ship.screen_rect.center
        ship.default_image = pygame.transform.smoothscale(ship.image_ship, settings.ship_size)

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_life()


def update_screen(settings, screen, ship,
                  text_update, bullets, explosion_sprites,
                  alien_sprites, play_button, stats, sb, rock_sprites, explosion_rock):
    # aplica cor ao fundo da janela
    screen.fill(settings.bg_color)
    screen.blit(settings.space_default_image, settings.space_rect)

    # A ORDEM DOS BLITS DEFINE ORDEM DE SOBREPOSIÇÂO DE CAMADAS

    # redesenha todas as balas atrás dos aliens e da nave
    for bullet in bullets.sprites():
        bullet.blitme()

    # redesenha objeto-eventos na tela a cada passagem do loop
    ship.blitme()
    alien_sprites.draw(screen)
    rock_sprites.draw(screen)
    explosion_sprites.draw(screen)
    explosion_rock.draw(screen)
    text_update.blitme()
    sb.show_score()

    if not stats.game_active:
        # inserir game over aqui
        play_button.draw_button()

    # redesenha texto a cada passagem do loop
    pygame.display.flip()


def update_bullets(settings, screen, bullets,
                   alien_sprites, explosion_sprites,
                   stats, sb, rock_sprites, explosion_rock):
    # atualiza tiro
    bullets.update()

    # se livra das balas qeu atravessaram a tela
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

        for alien_sprite in alien_sprites:
            collision = pygame.sprite.spritecollide(bullet, alien_sprites, True)
            if collision:
                bullets.remove(bullet)
                alien_sprites.remove(alien_sprite)
                explosion_sprites.add(Explosion(alien_sprite.rect.center))
                stats.score += settings.alien_points
                sb.prep_score()
                check_high_score(stats, sb)
                settings.actual_frame_explosion = settings.delay_frame_explosion

        collision_rock = pygame.sprite.spritecollide(bullet, rock_sprites, False)
        if collision_rock:
            bullets.remove(bullet)
            # rock_sprites.remove(rock_sprite)
            # explosion_rock.add(Explosion(rock_sprite.rect.center))
            # settings.actual_frame_explosion_rock = settings.delay_frame_explosion_rock

    # atualiza explosões
    update_bullet_alien_explosions(settings, explosion_sprites)
    # update_bullet_rock_explosions(settings, explosion_rock)


"""
def update_bullet_rock_explosions(settings, explosion_rock):
    if settings.actual_frame_explosion_rock > 0:
        settings.actual_frame_explosion_rock -= 1

    if settings.actual_frame_explosion_rock == 0:
        for explosion in explosion_rock:
            explosion_rock.remove(explosion)
        settings.actual_frame_explosion_rock = settings.delay_frame_explosion_rock

"""


def update_bullet_alien_explosions(settings, explosion_sprites):
    if settings.actual_frame_explosion > 0:
        settings.actual_frame_explosion -= 1

    if settings.actual_frame_explosion == 0:
        for explosion in explosion_sprites:
            explosion_sprites.remove(explosion)
        settings.actual_frame_explosion = settings.delay_frame_explosion


def fire_bullet(settings, screen, ship, bullets):
    # velocidade da bala = v. bala + v. nave
    if ship.move_up:
        settings = settings
        settings.bullet_speed += 0.1 * settings.ship_speed
    # limita qtd de tiros na tela
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)

        # Load audio file
        sound = mixer.Sound('images/blast.mp3')
        mixer.Sound.set_volume(sound, 0.5)
        # Play the music
        mixer.Sound.play(sound)

        bullets.add(new_bullet)


def update_ship_alien_explosions(settings, screen, ship,
                                 text_update, bullets, explosion_sprites,
                                 alien_sprites, stats, play_button, sb, rock_sprites, explosion_rock):
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, alien_sprites):
        ship.default_image = pygame.transform.smoothscale(ship.image_ship, (0, 0))
        explosion_sprites.add(Explosion(ship.rect.center))

        # Load audio file
        sound = mixer.Sound('images/explosion.mp3')
        mixer.Sound.set_volume(sound, 0.8)
        # Play the music
        mixer.Sound.play(sound)

        alien_sprites.empty()
        bullets.empty()

        update_screen(settings, screen, ship,
                      text_update, bullets, explosion_sprites,
                      alien_sprites, play_button, stats, sb, rock_sprites, explosion_rock)

        sleep(2)

        if stats.ships_left > 1:
            stats.ships_left -= 1
            sb.prep_life()
            bullets.empty()
            rock_sprites.empty()
            ship.rect.center = ship.screen_rect.center
            ship.default_image = pygame.transform.smoothscale(ship.image_ship, settings.ship_size)
        else:
            explosion_sprites.empty()
            explosion_rock.empty()
            bullets.empty()

            sb.life.empty()
            stats.game_active = False
            pygame.mouse.set_visible(True)


def update_ship_rock_explosions(settings, screen, ship, text_update,
                                bullets, explosion_sprites, alien_sprites,
                                stats, play_button, sb, rock_sprites, explosion_rock):
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, rock_sprites):
        ship.default_image = pygame.transform.smoothscale(ship.image_ship, (0, 0))
        explosion_rock.add(Explosion(ship.rect.center))

        # Load audio file
        sound = mixer.Sound('images/explosion.mp3')
        mixer.Sound.set_volume(sound, 0.8)
        # Play the music
        mixer.Sound.play(sound)

        alien_sprites.empty()
        bullets.empty()
        rock_sprites.empty()

        update_screen(settings, screen, ship,
                      text_update, bullets, explosion_sprites,
                      alien_sprites, play_button, stats, sb, rock_sprites, explosion_rock)

        sleep(2)

        if stats.ships_left > 1:
            stats.ships_left -= 1
            sb.prep_life()
            explosion_rock.empty()
            ship.rect.center = ship.screen_rect.center
            ship.default_image = pygame.transform.smoothscale(ship.image_ship, settings.ship_size)
        else:
            explosion_sprites.empty()
            explosion_rock.empty()
            bullets.empty()

            sb.life.empty()
            stats.game_active = False
            pygame.mouse.set_visible(True)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def alien_update(settings, screen, alien_sprites, bullets):
    # self.x += self.settings.alien_speed * self.settings.x_direction
    settings.actual_delay -= 1
    new_alien = alien.Alien(settings, screen)
    alien_sprites.update()

    if settings.actual_delay == 0:
        settings.actual_delay = settings.delay_set
        alien_sprites.add(new_alien)

    for one_alien in alien_sprites:
        if one_alien.rect.y >= settings.screen_height:
            alien_sprites.remove(one_alien)


def rock_update(settings, screen, rock_sprites, bullets):
    # self.x += self.settings.alien_speed * self.settings.x_direction
    settings.actual_delay_rock -= 1
    new_rock = rock.Rock(settings, screen)
    rock_sprites.update()

    if settings.actual_delay_rock == 0:
        settings.actual_delay_rock = settings.delay_set_rock
        rock_sprites.add(new_rock)

    for one_rock in rock_sprites:
        if one_rock.rect.y >= settings.screen_height:
            rock_sprites.remove(one_rock)
