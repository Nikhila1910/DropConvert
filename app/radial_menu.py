
import math

from PySide6.QtCore import Qt, Signal, QVariantAnimation
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QRadialGradient,
    QLinearGradient,
    QFont,
)
from PySide6.QtWidgets import QWidget


class RadialMenu(QWidget):

    file_dropped = Signal(str)
    format_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(520, 520)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)

        self.current_file = None
        self.active_format = None
        self.dragging_selection = False

        self.formats = ["PNG", "JPG"]

        self.hover_scale = 1.0

        # Animate the active glass bubble
        self.animation = QVariantAnimation(self)
        self.animation.setDuration(180)
        self.animation.valueChanged.connect(
            self.update_animation
        )

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def update_animation(self, value):
        self.hover_scale = float(value)
        self.update()

    def bubble_positions(self):

        cx = self.width() / 2
        cy = self.height() / 2

        radius = min(self.width(), self.height()) * 0.34

        positions = []

        for index, output_format in enumerate(self.formats):

            angle = math.radians(-90 + index * 360 / len(self.formats))

            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)

            positions.append({
                "format": output_format,
                "x": x,
                "y": y,
            })

        return positions

    def center_rect(self):

        cx = self.width() / 2
        cy = self.height() / 2

        radius = 72

        return (
            cx - radius,
            cy - radius,
            radius * 2,
            radius * 2,
        )

    def bubble_at(self, position):

        for item in self.bubble_positions():

            radius = 34

            if item["format"] == self.active_format:
                radius *= self.hover_scale

            distance = math.hypot(
                position.x() - item["x"],
                position.y() - item["y"],
            )

            if distance <= radius:
                return item["format"]

        return None

    def point_inside_center(self, position):

        cx = self.width() / 2
        cy = self.height() / 2

        distance = math.hypot(
            position.x() - cx,
            position.y() - cy,
        )

        return distance <= 72

    def animate_hover(self, new_format):

        if new_format == self.active_format:
            return

        self.active_format = new_format

        self.animation.stop()

        if new_format:
            self.animation.setStartValue(1.0)
            self.animation.setEndValue(1.28)
        else:
            self.animation.setStartValue(self.hover_scale)
            self.animation.setEndValue(1.0)

        self.animation.start()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        width = self.width()
        height = self.height()

        # Background gradient
        background = QLinearGradient(
            0, 0, width, height
        )

        background.setColorAt(
            0, QColor("#244E43")
        )

        background.setColorAt(
            0.45, QColor("#123C50")
        )

        background.setColorAt(
            1, QColor("#091B42")
        )

        painter.fillRect(
            self.rect(),
            background
        )

        # Background ambient light
        ambient = QRadialGradient(
            width * 0.25,
            height * 0.15,
            width * 0.8
        )

        ambient.setColorAt(
            0, QColor(100, 210, 145, 45)
        )

        ambient.setColorAt(
            1, QColor(20, 40, 90, 0)
        )

        painter.fillRect(
            self.rect(),
            ambient
        )

        # Decorative circular orbit
        cx = width / 2
        cy = height / 2

        orbit_radius = min(width, height) * 0.34

        painter.setPen(
            QPen(
                QColor(130, 205, 245, 45),
                1,
                Qt.PenStyle.DashLine
            )
        )

        painter.setBrush(Qt.BrushStyle.NoBrush)

        painter.drawEllipse(
            int(cx - orbit_radius),
            int(cy - orbit_radius),
            int(orbit_radius * 2),
            int(orbit_radius * 2)
        )

        # Draw the centre glass drop zone
        self.draw_glass_bubble(
            painter,
            cx,
            cy,
            72,
            False
        )

        painter.setPen(QColor("#FFFFFF"))

        center_font = QFont("Arial", 15)
        center_font.setBold(True)

        painter.setFont(center_font)

        if self.current_file:

            painter.drawText(
                int(cx - 60),
                int(cy - 8),
                120,
                28,
                Qt.AlignmentFlag.AlignCenter,
                "FILE READY"
            )

            painter.setFont(QFont("Arial", 10))

            painter.drawText(
                int(cx - 65),
                int(cy + 18),
                130,
                24,
                Qt.AlignmentFlag.AlignCenter,
                "Choose format"
            )

        else:

            painter.drawText(
                int(cx - 60),
                int(cy - 8),
                120,
                28,
                Qt.AlignmentFlag.AlignCenter,
                "+"
            )

            painter.setFont(QFont("Arial", 12))

            painter.drawText(
                int(cx - 65),
                int(cy + 20),
                130,
                25,
                Qt.AlignmentFlag.AlignCenter,
                "DROP FILE"
            )

        # Draw format bubbles
        for item in self.bubble_positions():

            output_format = item["format"]

            is_active = (
                output_format == self.active_format
            )

            radius = 34

            if is_active:
                radius *= self.hover_scale

            self.draw_glass_bubble(
                painter,
                item["x"],
                item["y"],
                radius,
                is_active
            )

            painter.setPen(
                QColor("#BCEBFF")
                if is_active
                else QColor("#D8EEFF")
            )

            font = QFont("Arial", 10)
            font.setBold(True)

            painter.setFont(font)

            painter.drawText(
                int(item["x"] - radius),
                int(item["y"] - 12),
                int(radius * 2),
                24,
                Qt.AlignmentFlag.AlignCenter,
                output_format
            )

        painter.end()

    def draw_glass_bubble(
        self,
        painter,
        x,
        y,
        radius,
        active
    ):

        painter.save()

        # Outer glow
        if active:

            painter.setPen(
                QPen(
                    QColor(100, 200, 255, 130),
                    5
                )
            )

            painter.setBrush(Qt.BrushStyle.NoBrush)

            painter.drawEllipse(
                int(x - radius - 4),
                int(y - radius - 4),
                int((radius + 4) * 2),
                int((radius + 4) * 2)
            )

        # Glass gradient
        glass = QRadialGradient(
            x - radius * 0.35,
            y - radius * 0.45,
            radius * 2
        )

        if active:

            glass.setColorAt(
                0, QColor(180, 235, 255, 105)
            )

            glass.setColorAt(
                1, QColor(60, 130, 220, 75)
            )

        else:

            glass.setColorAt(
                0, QColor(180, 230, 240, 65)
            )

            glass.setColorAt(
                1, QColor(40, 100, 170, 35)
            )

        painter.setBrush(glass)

        painter.setPen(
            QPen(
                QColor(160, 225, 255, 165),
                1.3
            )
        )

        painter.drawEllipse(
            int(x - radius),
            int(y - radius),
            int(radius * 2),
            int(radius * 2)
        )

        # Small glass reflection
        painter.setPen(Qt.PenStyle.NoPen)

        painter.setBrush(
            QColor(255, 255, 255, 20)
        )

        painter.drawEllipse(
            int(x - radius * 0.48),
            int(y - radius * 0.62),
            int(radius * 0.75),
            int(radius * 0.35)
        )

        painter.restore()

    # Drag a file from Finder onto the application
    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):

        if event.mimeData().hasUrls():

            if self.point_inside_center(event.position()):

                event.acceptProposedAction()

            else:

                event.ignore()

        else:

            event.ignore()

    def dropEvent(self, event):

        urls = event.mimeData().urls()

        if not urls:
            return

        file_path = urls[0].toLocalFile()

        if not file_path:
            event.ignore()
            return

        self.current_file = file_path

        self.file_dropped.emit(file_path)

        self.update()

        event.acceptProposedAction()

    # Hover over a format bubble
    def mouseMoveEvent(self, event):

        target = self.bubble_at(event.position())

        self.animate_hover(target)

        super().mouseMoveEvent(event)

    # Click or begin dragging from the centre
    def mousePressEvent(self, event):

        if event.button() != Qt.MouseButton.LeftButton:
            return

        if self.current_file and self.point_inside_center(
            event.position()
        ):

            self.dragging_selection = True
            return

        target = self.bubble_at(event.position())

        if target and self.current_file:
            self.format_selected.emit(target)

    # Release the drag on an output bubble
    def mouseReleaseEvent(self, event):

        if (
            event.button() == Qt.MouseButton.LeftButton
            and self.dragging_selection
        ):

            target = self.bubble_at(event.position())

            if target and self.current_file:
                self.format_selected.emit(target)

            self.dragging_selection = False

        super().mouseReleaseEvent(event)

    def leaveEvent(self, event):

        self.animate_hover(None)

        super().leaveEvent(event)
