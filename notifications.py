from plyer import notification


def show_notification(title, message):
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=10
        )
    except Exception as error:
        print("Error mostrando notificación:", error)