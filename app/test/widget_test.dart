import 'package:flutter_test/flutter_test.dart';
import 'package:chat_com/main.dart';

void main() {
  testWidgets('shows the Chat.com navigation', (tester) async {
    await tester.pumpWidget(const ChatComApp());
    expect(find.text('Chat.com'), findsOneWidget);
    expect(find.text('Chats'), findsWidgets);
    expect(find.text('Contacts'), findsOneWidget);
    expect(find.text('Settings'), findsOneWidget);
  });

  testWidgets('opens a conversation and sends a local message', (tester) async {
    await tester.pumpWidget(const ChatComApp());
    await tester.tap(find.text('Aarav Sharma').first);
    await tester.pumpAndSettle();
    expect(find.text('Preview conversation'), findsOneWidget);
    await tester.enterText(find.byType(TextField).last, 'Hello from the test');
    await tester.tap(find.byTooltip('Send message'));
    await tester.pump();
    expect(find.text('Hello from the test'), findsOneWidget);
  });
}
