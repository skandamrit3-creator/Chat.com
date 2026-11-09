import 'package:flutter/material.dart';

void main() => runApp(const ChatComApp());

const _brand = Color(0xFF087F68);
const _ink = Color(0xFF172A26);
const _muted = Color(0xFF75827E);
const _canvas = Color(0xFFF5F8F6);

class ChatComApp extends StatelessWidget {
  const ChatComApp({super.key});

  @override
  Widget build(BuildContext context) {
    final scheme = ColorScheme.fromSeed(seedColor: _brand);
    return MaterialApp(
      title: 'Chat.com',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: scheme,
        scaffoldBackgroundColor: _canvas,
        appBarTheme: const AppBarTheme(backgroundColor: _canvas, foregroundColor: _ink, elevation: 0),
        textTheme: ThemeData.light().textTheme.apply(bodyColor: _ink, displayColor: _ink),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.white,
          hintStyle: const TextStyle(color: _muted),
          contentPadding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(18), borderSide: BorderSide.none),
        ),
      ),
      home: const ChatHomePage(),
    );
  }
}

class ChatHomePage extends StatefulWidget {
  const ChatHomePage({super.key});
  @override
  State<ChatHomePage> createState() => _ChatHomePageState();
}

class _ChatHomePageState extends State<ChatHomePage> {
  int _selectedIndex = 0;

  void _openConversation(String name, String initials, Color color) {
    Navigator.of(context).push(MaterialPageRoute<void>(
      builder: (_) => ConversationPage(contactName: name, initials: initials, avatarColor: color),
    ));
  }

  @override
  Widget build(BuildContext context) {
    final pages = <Widget>[
      ChatsPage(onOpenConversation: _openConversation),
      ContactsPage(onOpenConversation: _openConversation),
      const SettingsPage(),
    ];
    return Scaffold(
      body: SafeArea(child: IndexedStack(index: _selectedIndex, children: pages)),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (index) => setState(() => _selectedIndex = index),
        backgroundColor: Colors.white,
        indicatorColor: const Color(0xFFDDF3EC),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.chat_bubble_outline_rounded), selectedIcon: Icon(Icons.chat_bubble_rounded), label: 'Chats'),
          NavigationDestination(icon: Icon(Icons.people_outline_rounded), selectedIcon: Icon(Icons.people_rounded), label: 'Contacts'),
          NavigationDestination(icon: Icon(Icons.settings_outlined), selectedIcon: Icon(Icons.settings_rounded), label: 'Settings'),
        ],
      ),
    );
  }
}

class _ChatPreview {
  const _ChatPreview(this.name, this.message, this.time, this.initials, this.color, this.unread);
  final String name;
  final String message;
  final String time;
  final String initials;
  final Color color;
  final int unread;
}

class ChatsPage extends StatelessWidget {
  const ChatsPage({super.key, required this.onOpenConversation});
  final void Function(String, String, Color) onOpenConversation;

  static const _chats = <_ChatPreview>[
    _ChatPreview('Aarav Sharma', 'Are we still meeting today?', '10:42', 'AS', Color(0xFFDAE9FF), 2),
    _ChatPreview('Maya Verma', 'That photo looks amazing!', '09:18', 'MV', Color(0xFFFFE7D7), 0),
    _ChatPreview('Project Team', 'Rohan: I have shared the notes', 'Yesterday', 'PT', Color(0xFFE9E1FF), 4),
    _ChatPreview('Kabir Singh', 'Voice message', 'Yesterday', 'KS', Color(0xFFDDF1E7), 0),
    _ChatPreview('Ananya Das', 'Thank you 😊', 'Monday', 'AD', Color(0xFFFFE2EC), 0),
  ];

  @override
  Widget build(BuildContext context) {
    return CustomScrollView(slivers: [
      SliverPadding(
        padding: const EdgeInsets.fromLTRB(22, 18, 22, 12),
        sliver: SliverToBoxAdapter(child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(children: [
              Container(
                width: 42, height: 42,
                decoration: BoxDecoration(color: const Color(0xFFDDF3EC), borderRadius: BorderRadius.circular(15)),
                child: const Icon(Icons.forum_rounded, color: _brand, size: 23),
              ),
              const SizedBox(width: 12),
              const Expanded(child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Chat.com', style: TextStyle(fontSize: 23, fontWeight: FontWeight.w800, letterSpacing: -0.7)),
                  Text('Your conversations, together', style: TextStyle(fontSize: 12, color: _muted)),
                ],
              )),
              IconButton(tooltip: 'New message', onPressed: () => _showPreviewNotice(context, 'New message'), icon: const Icon(Icons.edit_outlined, color: _brand)),
            ]),
            const SizedBox(height: 25),
            const Text('Messages', style: TextStyle(fontSize: 29, fontWeight: FontWeight.w800)),
            const SizedBox(height: 15),
            TextField(
              readOnly: true,
              onTap: () => showSearch<void>(context: context, delegate: _ChatSearchDelegate(_chats)),
              decoration: const InputDecoration(hintText: 'Search conversations', prefixIcon: Icon(Icons.search_rounded, color: _muted), suffixIcon: Icon(Icons.tune_rounded, color: _muted)),
            ),
            const SizedBox(height: 20),
            const Row(children: [
              Text('RECENT CHATS', style: TextStyle(color: _muted, fontSize: 11, fontWeight: FontWeight.w800, letterSpacing: 1.2)),
              Spacer(),
              Text('Preview', style: TextStyle(color: _brand, fontSize: 12, fontWeight: FontWeight.w700)),
            ]),
            const SizedBox(height: 8),
          ],
        )),
      ),
      SliverPadding(
        padding: const EdgeInsets.symmetric(horizontal: 14),
        sliver: SliverList(delegate: SliverChildBuilderDelegate((context, index) {
          final chat = _chats[index];
          return _ChatTile(chat: chat, onTap: () => onOpenConversation(chat.name, chat.initials, chat.color));
        }, childCount: _chats.length)),
      ),
      const SliverToBoxAdapter(child: SizedBox(height: 24)),
    ]);
  }
}

class _ChatTile extends StatelessWidget {
  const _ChatTile({required this.chat, required this.onTap});
  final _ChatPreview chat;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => Material(
    color: Colors.transparent,
    child: InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(18),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 12),
        child: Row(children: [
          _Avatar(initials: chat.initials, color: chat.color, size: 54),
          const SizedBox(width: 13),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(chat.name, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 15)),
            const SizedBox(height: 5),
            Text(chat.message, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(color: _muted, fontSize: 12.5)),
          ])),
          const SizedBox(width: 8),
          Column(crossAxisAlignment: CrossAxisAlignment.end, children: [
            Text(chat.time, style: const TextStyle(color: _muted, fontSize: 10.5)),
            const SizedBox(height: 8),
            if (chat.unread > 0)
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 3),
                decoration: BoxDecoration(color: _brand, borderRadius: BorderRadius.circular(20)),
                child: Text('${chat.unread}', style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.w700)),
              )
            else
              const SizedBox(height: 17),
          ]),
        ]),
      ),
    ),
  );
}

class ContactsPage extends StatelessWidget {
  const ContactsPage({super.key, required this.onOpenConversation});
  final void Function(String, String, Color) onOpenConversation;
  static const contacts = <_ChatPreview>[
    _ChatPreview('Aarav Sharma', 'Available', '', 'AS', Color(0xFFDAE9FF), 0),
    _ChatPreview('Maya Verma', 'At work', '', 'MV', Color(0xFFFFE7D7), 0),
    _ChatPreview('Kabir Singh', 'Hey there! I am using Chat.com', '', 'KS', Color(0xFFDDF1E7), 0),
    _ChatPreview('Ananya Das', 'Available', '', 'AD', Color(0xFFFFE2EC), 0),
    _ChatPreview('Rohan Kumar', 'Busy', '', 'RK', Color(0xFFE9E1FF), 0),
  ];

  @override
  Widget build(BuildContext context) => ListView(
    padding: const EdgeInsets.fromLTRB(22, 22, 22, 24),
    children: [
      const Text('Contacts', style: TextStyle(fontSize: 29, fontWeight: FontWeight.w800)),
      const SizedBox(height: 7),
      const Text('People you can connect with', style: TextStyle(color: _muted, fontSize: 13)),
      const SizedBox(height: 20),
      const TextField(decoration: InputDecoration(hintText: 'Find a contact', prefixIcon: Icon(Icons.search_rounded))),
      const SizedBox(height: 17),
      ...contacts.map((contact) => ListTile(
        contentPadding: const EdgeInsets.symmetric(vertical: 5),
        leading: _Avatar(initials: contact.initials, color: contact.color, size: 48),
        title: Text(contact.name, style: const TextStyle(fontWeight: FontWeight.w700)),
        subtitle: Text(contact.message, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(color: _muted, fontSize: 12)),
        trailing: IconButton(
          tooltip: 'Message ${contact.name}',
          onPressed: () => onOpenConversation(contact.name, contact.initials, contact.color),
          icon: const Icon(Icons.chat_bubble_outline, color: _brand),
        ),
        onTap: () => onOpenConversation(contact.name, contact.initials, contact.color),
      )),
    ],
  );
}

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});
  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  bool _notifications = true;
  bool _readReceipts = true;

  @override
  Widget build(BuildContext context) => ListView(
    padding: const EdgeInsets.fromLTRB(22, 22, 22, 28),
    children: [
      const Text('Settings', style: TextStyle(fontSize: 29, fontWeight: FontWeight.w800)),
      const SizedBox(height: 20),
      Container(
        padding: const EdgeInsets.all(17),
        decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(22)),
        child: const Row(children: [
          _Avatar(initials: 'SK', color: Color(0xFFDDF3EC), size: 58),
          SizedBox(width: 14),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text('Your profile', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
            SizedBox(height: 4),
            Text('Set up your name and photo', style: TextStyle(color: _muted, fontSize: 12)),
          ])),
          Icon(Icons.chevron_right_rounded, color: _muted),
        ]),
      ),
      const SizedBox(height: 22),
      const _SettingsSectionTitle('PREFERENCES'),
      SwitchListTile(contentPadding: EdgeInsets.zero, value: _notifications, onChanged: (value) => setState(() => _notifications = value), secondary: const Icon(Icons.notifications_none_rounded), title: const Text('Notifications'), subtitle: const Text('Message alerts on this device')),
      SwitchListTile(contentPadding: EdgeInsets.zero, value: _readReceipts, onChanged: (value) => setState(() => _readReceipts = value), secondary: const Icon(Icons.done_all_rounded), title: const Text('Read receipts'), subtitle: const Text('Show when messages are read')),
      const SizedBox(height: 12),
      const _SettingsSectionTitle('ACCOUNT & SUPPORT'),
      const _SettingsRow(icon: Icons.lock_outline_rounded, title: 'Privacy and security'),
      const _SettingsRow(icon: Icons.devices_rounded, title: 'Linked devices'),
      const _SettingsRow(icon: Icons.help_outline_rounded, title: 'Help and support'),
      const SizedBox(height: 18),
      const Center(child: Text('Chat.com  •  Preview 0.1.0', style: TextStyle(color: _muted, fontSize: 11))),
    ],
  );
}

class _SettingsSectionTitle extends StatelessWidget {
  const _SettingsSectionTitle(this.title);
  final String title;
  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 8),
    child: Text(title, style: const TextStyle(color: _muted, fontSize: 11, fontWeight: FontWeight.w800, letterSpacing: 1.1)),
  );
}

class _SettingsRow extends StatelessWidget {
  const _SettingsRow({required this.icon, required this.title});
  final IconData icon;
  final String title;
  @override
  Widget build(BuildContext context) => ListTile(
    contentPadding: EdgeInsets.zero,
    leading: Icon(icon, color: _ink),
    title: Text(title, style: const TextStyle(fontSize: 14)),
    trailing: const Icon(Icons.chevron_right_rounded, color: _muted),
    onTap: () {},
  );
}

class _Avatar extends StatelessWidget {
  const _Avatar({required this.initials, required this.color, required this.size});
  final String initials;
  final Color color;
  final double size;
  @override
  Widget build(BuildContext context) => CircleAvatar(
    radius: size / 2,
    backgroundColor: color,
    child: Text(initials, style: const TextStyle(color: _ink, fontWeight: FontWeight.w800, fontSize: 14)),
  );
}

class ConversationPage extends StatefulWidget {
  const ConversationPage({super.key, required this.contactName, required this.initials, required this.avatarColor});
  final String contactName;
  final String initials;
  final Color avatarColor;
  @override
  State<ConversationPage> createState() => _ConversationPageState();
}

class _ConversationPageState extends State<ConversationPage> {
  final _controller = TextEditingController();
  final List<_Message> _messages = [
    const _Message('Hi! Welcome to this Chat.com preview.', false, '10:38'),
    const _Message('This is looking good 👋', true, '10:40'),
    const _Message('You can type and send a message below.', false, '10:41'),
  ];

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _sendMessage() {
    final value = _controller.text.trim();
    if (value.isEmpty) return;
    setState(() {
      _messages.add(_Message(value, true, 'Now'));
      _controller.clear();
    });
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(
      backgroundColor: Colors.white,
      leadingWidth: 42,
      titleSpacing: 4,
      title: Row(children: [
        _Avatar(initials: widget.initials, color: widget.avatarColor, size: 38),
        const SizedBox(width: 10),
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(widget.contactName, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w800)),
          const Text('Preview conversation', style: TextStyle(color: _muted, fontSize: 10)),
        ])),
      ]),
      actions: [
        IconButton(tooltip: 'Voice call (coming later)', onPressed: () => _showPreviewNotice(context, 'Voice calls'), icon: const Icon(Icons.call_outlined)),
        IconButton(tooltip: 'More options', onPressed: () => _showPreviewNotice(context, 'Chat options'), icon: const Icon(Icons.more_vert_rounded)),
      ],
    ),
    body: Column(children: [
      Expanded(child: ListView.builder(
        padding: const EdgeInsets.fromLTRB(16, 20, 16, 16),
        itemCount: _messages.length,
        itemBuilder: (context, index) {
          final message = _messages[index];
          return Align(
            alignment: message.outgoing ? Alignment.centerRight : Alignment.centerLeft,
            child: Container(
              constraints: BoxConstraints(maxWidth: MediaQuery.sizeOf(context).width * 0.78),
              margin: const EdgeInsets.only(bottom: 10),
              padding: const EdgeInsets.fromLTRB(14, 11, 12, 8),
              decoration: BoxDecoration(
                color: message.outgoing ? const Color(0xFFDDF3EC) : Colors.white,
                borderRadius: BorderRadius.only(
                  topLeft: const Radius.circular(18),
                  topRight: const Radius.circular(18),
                  bottomLeft: Radius.circular(message.outgoing ? 18 : 5),
                  bottomRight: Radius.circular(message.outgoing ? 5 : 18),
                ),
              ),
              child: Column(crossAxisAlignment: CrossAxisAlignment.end, children: [
                Align(alignment: Alignment.centerLeft, child: Text(message.text, style: const TextStyle(fontSize: 14))),
                const SizedBox(height: 4),
                Text(message.time, style: const TextStyle(color: _muted, fontSize: 9)),
              ]),
            ),
          );
        },
      )),
      SafeArea(top: false, child: Container(
        color: Colors.white,
        padding: const EdgeInsets.fromLTRB(12, 10, 12, 10),
        child: Row(crossAxisAlignment: CrossAxisAlignment.end, children: [
          IconButton(tooltip: 'Attachments (coming later)', onPressed: () => _showPreviewNotice(context, 'Attachments'), icon: const Icon(Icons.add_circle_outline, color: _brand)),
          Expanded(child: TextField(
            controller: _controller,
            minLines: 1,
            maxLines: 4,
            textCapitalization: TextCapitalization.sentences,
            onSubmitted: (_) => _sendMessage(),
            decoration: InputDecoration(
              hintText: 'Write a message...',
              filled: true,
              fillColor: _canvas,
              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(22), borderSide: BorderSide.none),
            ),
          )),
          const SizedBox(width: 8),
          IconButton.filled(
            tooltip: 'Send message',
            onPressed: _sendMessage,
            style: IconButton.styleFrom(backgroundColor: _brand, foregroundColor: Colors.white),
            icon: const Icon(Icons.arrow_upward_rounded),
          ),
        ]),
      )),
    ]),
  );
}

class _Message {
  const _Message(this.text, this.outgoing, this.time);
  final String text;
  final bool outgoing;
  final String time;
}

class _ChatSearchDelegate extends SearchDelegate<void> {
  _ChatSearchDelegate(this.chats);
  final List<_ChatPreview> chats;
  @override
  String get searchFieldLabel => 'Search chats';
  @override
  List<Widget> buildActions(BuildContext context) => [
    IconButton(onPressed: () => query = '', icon: const Icon(Icons.clear_rounded)),
  ];
  @override
  Widget buildLeading(BuildContext context) => IconButton(onPressed: () => close(context, null), icon: const Icon(Icons.arrow_back_rounded));
  @override
  Widget buildResults(BuildContext context) => _buildMatches();
  @override
  Widget buildSuggestions(BuildContext context) => _buildMatches();

  Widget _buildMatches() {
    final matches = chats.where((chat) =>
      chat.name.toLowerCase().contains(query.toLowerCase()) ||
      chat.message.toLowerCase().contains(query.toLowerCase())).toList();
    if (matches.isEmpty) return const Center(child: Text('No matching conversations'));
    return ListView(children: matches.map((chat) => ListTile(
      leading: _Avatar(initials: chat.initials, color: chat.color, size: 44),
      title: Text(chat.name),
      subtitle: Text(chat.message),
    )).toList());
  }
}

void _showPreviewNotice(BuildContext context, String feature) {
  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$feature will be added in a later upgrade.')));
}
