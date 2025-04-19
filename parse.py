from datetime import timezone, datetime
import flet as ft
import requests

def main(page: ft.Page):
    page.title = 'Discord Parsing Tool'
    page.theme_mode = 'light'
    page.window.height = 600
    page.window.width = 650
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.resizable = False
    user_id = False

    def parse(e):
        nonlocal user_id

        def error(msg):
            errors.color = '#FF0000'
            errors.value = msg

        formats = ['png', 'gif', 'jpg']
        data = {
            'user_id': '',
            'avatar_url': '',
            'banner_url': '',
            'created_at': ''
        }

        raw_input = textfield.value.strip()

        if not raw_input:
            error('Please, enter ID')
        else:
            try:
                user_id = int(raw_input)
                errors.color = '#000000'
                errors.value = ''

                data['user_id'] = user_id
                for f in formats:
                    avatar_url = f'https://cdn.discordapp.com/avatars/{user_id}/avatar.{f}?size=1024'
                    r = requests.get(avatar_url)
                    if r.status_code == 200:
                        data['avatar_url'] = avatar_url
                        break
                    else:
                        data['avatar_url'] = 'Not found'

                for f in formats:
                    banner_url = f'https://cdn.discordapp.com/banners/{user_id}/banner.{f}?size=1024'
                    r = requests.get(banner_url)
                    if r.status_code == 200:
                        data['banner_url'] = banner_url
                        break
                    else:
                        data['banner_url'] = 'Not found'

                discord_epoch = 1420070400000
                timestamp = ((user_id >> 22) + discord_epoch) / 1000
                data['created_at'] = datetime.fromtimestamp(timestamp, tz=timezone.utc)


                results.value = (f'''User ID : {data["user_id"]}
Account created at : {data["created_at"]}
Avatar url : {data.get("avatar_url")}
Banner url : {data.get("banner_url")}
Snowflake lookup : https://discordlookup.com/user/{data["user_id"]}
Discord tracker : https://discord-tracker.com/tracker/user/{data["user_id"]}/''')
                
            except ValueError:
                error('Please, enter a valid numeric ID')



        page.update()

    title = ft.Text(
        'Discord Parsing Tool',
        size=50
    )

    textfield = ft.TextField(
        hint_text='Enter ID',
        width=500
    )

    button = ft.ElevatedButton(
        text='Submit',
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
        width = 85,
        on_click=parse
    )

    errors = ft.Text('')

    results = ft.TextField(
        read_only=True,
        hint_text='Results',
        width=600,
        multiline=True
    )

    page.add(ft.Row([title], alignment=ft.MainAxisAlignment.CENTER))
    page.add(ft.Row([textfield, button]))
    page.add(ft.Row([errors]))
    page.add(ft.Row([results]))

ft.app(target=main)
