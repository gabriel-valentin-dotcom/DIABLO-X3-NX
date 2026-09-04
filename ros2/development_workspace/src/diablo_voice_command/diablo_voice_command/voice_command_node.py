#!/usr/bin/env python3

import re
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class VoiceCommandNode(Node):

    def __init__(self):
        super().__init__('voice_command_node')

        self.wake_active_until = 0.0
        self.wake_window_sec = 15.0

        self.last_pose_intent = None
        self.last_pose_publish_time = 0.0
        self.pose_duplicate_window_sec = 2.0

        self.wake_words = [
            'diablo',
            'diabloo',
            'du diablo',
            'hallo diablo',
            'hei diablo',
            'hai diablo',
            'hey diablo',
            'dia blo',
            'diabolo',
            'dialog',
            'die ablo',
            'dieablo',
            'the ablo',
            'tiablo',
        ]

        self.sub = self.create_subscription(
            String,
            '/voice_text',
            self.on_voice_text,
            10
        )

        self.cmd_pub = self.create_publisher(
            String,
            '/voice_cmd_de',
            10
        )

        self.feedback_pub = self.create_publisher(
            String,
            '/diablo_feedback',
            10
        )

        self.get_logger().info(
            'Voice Command Node FINAL aktiv: STOP immer aktiv + Wakeword + Cooldown'
        )

    def feedback_beep(self):
        msg = String()
        msg.data = 'BEEP'
        self.feedback_pub.publish(msg)

    def publish_cmd(self, cmd, original):
        now = time.monotonic()
        pose_intents = {'STAND_UP', 'SIT_DOWN'}
        short_motion_intents = {
            'FORWARD_SHORT', 'BACKWARD_SHORT', 'TURN_LEFT_SHORT', 'TURN_RIGHT',
        }

        if (
            cmd in pose_intents
            and cmd == self.last_pose_intent
            and now - self.last_pose_publish_time < self.pose_duplicate_window_sec
        ):
            age_sec = now - self.last_pose_publish_time
            self.get_logger().info(
                f'VOICE_COMMAND_DUPLICATE_SUPPRESSED intent={cmd} '
                f'age_sec={age_sec:.3f}'
            )
            return

        msg = String()
        msg.data = cmd

        self.cmd_pub.publish(msg)

        if cmd in short_motion_intents:
            self.get_logger().info(
                f'INTERACT_SHORT_TRACE_INTENT input="{original}" intent={cmd}'
            )

        if cmd in pose_intents:
            self.last_pose_intent = cmd
            self.last_pose_publish_time = now
            self.get_logger().info(
                f'VOICE_COMMAND_PUBLISHED intent={cmd} topic=/voice_cmd_de'
            )

        self.get_logger().warn(
            f'VOICE CMD: {original} -> {cmd}'
        )

    def normalize(self, text):

        text = text.strip().lower()

        replacements = {
            'ß': 'ss',
            ',': '',
            '.': '',
            '!': '',
            '?': '',
        }

        for a, b in replacements.items():
            text = text.replace(a, b)

        phrase_replacements = {
            'die upload': 'diablo',
            'die able': 'diablo',
            'die abele': 'diablo',
            'einschaltet': 'einschalten',
            'ausschaltet': 'ausschalten',
            'setze dich': 'setz dich',
            'setzt dich': 'setz dich',
            'stehe auf': 'steh auf',
        }

        for a, b in phrase_replacements.items():
            text = text.replace(a, b)

        return ' '.join(text.split())

    def has_wakeword(self, text):

        return any(w in text for w in self.wake_words)

    def map_command(self, text):

        # STOP IMMER AKTIV
        stop_words = [
            'stop',
            'stopp',
            'halt',
            'anhalten',
        ]

        if text in stop_words:
            return 'STOP'

        # SIT DOWN
        sit_words = [
            'setz dich',
            'sitz',
        ]

        if text in sit_words:
            return 'SIT_DOWN'

        # STAND UP
        stand_words = [
            'steh auf',
            'stehe auf',
            'aufstehen',
        ]

        if text in stand_words:
            return 'STAND_UP'

        return None

    @staticmethod
    def map_body_command(text):
        return {
            'höher': 'HEIGHT_HIGH',
            'geh höher': 'HEIGHT_HIGH',
            'mach dich höher': 'HEIGHT_HIGH',
            'tiefer': 'HEIGHT_LOW',
            'geh tiefer': 'HEIGHT_LOW',
            'mach dich tiefer': 'HEIGHT_LOW',
            'normale höhe': 'HEIGHT_MID',
            'mittlere höhe': 'HEIGHT_MID',
            'auf normale höhe': 'HEIGHT_MID',
            'neig dich nach links': 'LEAN_LEFT',
            'lehn dich nach links': 'LEAN_LEFT',
            'neig dich nach rechts': 'LEAN_RIGHT',
            'lehn dich nach rechts': 'LEAN_RIGHT',
            'gerade': 'LEAN_CENTER',
            'stell dich gerade': 'LEAN_CENTER',
            'körper gerade': 'LEAN_CENTER',
            'schau nach oben': 'PITCH_UP',
            'schau hoch': 'PITCH_UP',
            'schau nach unten': 'PITCH_DOWN',
            'schau runter': 'PITCH_DOWN',
            'schau geradeaus': 'PITCH_CENTER',
            'kopf gerade': 'PITCH_CENTER',
            'schau gerade': 'PITCH_CENTER',
        }.get(text)

    @staticmethod
    def map_turn_right_command(text):
        """Map only the approved single-shot right-turn voice variants."""
        return {
            'dreh dich rechts': 'TURN_RIGHT',
            'dreh dich nach rechts': 'TURN_RIGHT',
            'dreh rechts': 'TURN_RIGHT',
            'nach rechts drehen': 'TURN_RIGHT',
        }.get(text)

    @classmethod
    def map_short_motion_command(cls, text):
        """Map only the four approved single-shot motion voice variants."""
        return cls.map_turn_right_command(text) or {
            'fahr langsam vor': 'FORWARD_SHORT',
            'fahr vor': 'FORWARD_SHORT',
            'langsam vor': 'FORWARD_SHORT',
            'fahre langsam vor': 'FORWARD_SHORT',
            'fahr ein stück vor': 'FORWARD_SHORT',
            'geh ein stück vor': 'FORWARD_SHORT',
            'fahr langsam zurück': 'BACKWARD_SHORT',
            'fahr zurück': 'BACKWARD_SHORT',
            'langsam zurück': 'BACKWARD_SHORT',
            'fahre langsam zurück': 'BACKWARD_SHORT',
            'fahr ein stück zurück': 'BACKWARD_SHORT',
            'geh ein stück zurück': 'BACKWARD_SHORT',
            'dreh dich links': 'TURN_LEFT_SHORT',
            'dreh dich nach links': 'TURN_LEFT_SHORT',
            'dreh links': 'TURN_LEFT_SHORT',
            'nach links drehen': 'TURN_LEFT_SHORT',
        }.get(text)

    @staticmethod
    def has_explicit_diablo_wakeword(text):
        return bool(re.search(r'\bdiablo\b', text))

    def on_voice_text(self, msg):

        original = msg.data.strip()
        text = self.normalize(original)

        if not text:
            return

        self.get_logger().info(f'VOICE_TEXT_RECEIVED text="{original}"')

        now = time.time()

        # STOP IMMER DIREKT
        stop_cmd = self.map_command(text)

        if stop_cmd == 'STOP':
            self.publish_cmd('STOP', original)
            return

        if stop_cmd in {'STAND_UP', 'SIT_DOWN'}:
            self.get_logger().info(
                f'VOICE_COMMAND_MATCH input="{text}" intent={stop_cmd}'
            )
            self.publish_cmd(stop_cmd, original)
            return

        context_stop_words = {
            'warte',
            'warte bitte',
            'bleib',
            'bleib da',
            'nein',
            'ruhig',
        }

        # WAKEWORD
        if self.has_wakeword(text):

            self.wake_active_until = now + self.wake_window_sec

            self.feedback_beep()

            self.get_logger().info(
                'WAKEWORD OK: nur Beep, 10s Befehlsfenster aktiv'
            )

            cleaned = text

            for wake in sorted(self.wake_words, key=len, reverse=True):
                cleaned = cleaned.replace(wake, '').strip()

            cmd = 'STOP' if cleaned in context_stop_words else self.map_command(cleaned)
            if cmd is None and self.has_explicit_diablo_wakeword(text):
                cmd = (
                    self.map_short_motion_command(cleaned)
                    or self.map_body_command(cleaned)
                )

            if cmd:
                self.publish_cmd(cmd, original)
                self.wake_active_until = 0.0

            return

        # WAKE AKTIV
        if now <= self.wake_active_until:

            cmd = 'STOP' if text in context_stop_words else self.map_command(text)

            if cmd:
                self.publish_cmd(cmd, original)
                self.wake_active_until = 0.0
                return

            self.get_logger().info(
                f'WAKE AKTIV aber kein gültiger Befehl: {original}'
            )

            return

        self.get_logger().info(
            f'IGNORIERT ohne Wakeword: {original}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = VoiceCommandNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
