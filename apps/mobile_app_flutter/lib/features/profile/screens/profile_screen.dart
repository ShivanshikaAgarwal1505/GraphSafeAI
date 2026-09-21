import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../auth/providers/auth_provider.dart';

import '../../auth/screens/login_screen.dart';
import '../../auth/screens/register_screen.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    final auth =
        context.watch<AuthProvider>();

    final user = auth.user;

    if (user == null) {
      return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Profile',
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment:
              MainAxisAlignment.center,
          children: [
            const CircleAvatar(
              radius: 50,
              child: Icon(
                Icons.person,
                size: 50,
              ),
            ),

            const SizedBox(
              height: 24,
            ),

            Text(
              'Welcome to GraphSafeAI',
              style: Theme.of(context)
                  .textTheme
                  .headlineSmall,
              textAlign: TextAlign.center,
            ),

            const SizedBox(
              height: 12,
            ),

            Text(
              'Sign in to save favorite places, track your reports and build your reputation.',
              textAlign: TextAlign.center,
              style: TextStyle(
                color: Colors.grey[700],
              ),
            ),

            const SizedBox(
              height: 32,
            ),

            SizedBox(
              width: double.infinity,
              child: FilledButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) =>LoginScreen(),
                    ),
                  );
                },
                child: const Text(
                  'Login',
                ),
              ),
            ),

            const SizedBox(
              height: 12,
            ),

            SizedBox(
              width: double.infinity,
              child: OutlinedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) =>
                        const RegisterScreen(),
                    ),
                  );
                },
                child: const Text(
                  'Create Account',
                ),
              ),
            ),
          ],
        ),
      ),
    );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Profile',
        ),
      ),
      body: Padding(
        padding:
            const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment:
              CrossAxisAlignment.start,
          children: [
            Text(
              user.name,
              style: Theme.of(context)
                  .textTheme
                  .headlineSmall,
            ),

            const SizedBox(
              height: 8,
            ),

            Text(user.email),

            const SizedBox(
              height: 24,
            ),

            Card(
              child: ListTile(
                title: const Text(
                  'Reputation',
                ),
                trailing: Text(
                  user.reputationScore
                      .toString(),
                ),
              ),
            ),

            Card(
              child: ListTile(
                title: const Text(
                  'Reports Submitted',
                ),
                trailing: Text(
                  user.reportsSubmitted
                      .toString(),
                ),
              ),
            ),

            Card(
              child: ListTile(
                title: const Text(
                  'Reports Verified',
                ),
                trailing: Text(
                  user.reportsVerified
                      .toString(),
                ),
              ),
            ),

            ListTile(
              leading: const Icon(
                Icons.list_alt,
              ),
              title: const Text(
                'My Reports',
              ),
              subtitle: const Text(
                'View reports you submitted',
              ),
              onTap: () {
    // next screen later
              },
            ),
            
            const SizedBox(
              height: 20,
            ),

            ElevatedButton(
              onPressed: () async {
                await auth.logout();
              },
              child: const Text(
                'Logout',
              ),
            ),
          ],
        ),
      ),
    );
  }
}