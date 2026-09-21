import 'package:flutter/material.dart';

import '../features/navigation/screens/home_screen.dart';
import '../features/reports/screens/reports_screen.dart';
import '../features/profile/screens/profile_screen.dart';

class MainNavigation extends StatefulWidget {
  const MainNavigation({
    super.key,
  });

  @override
  State<MainNavigation> createState() =>
      _MainNavigationState();
}

class _MainNavigationState
    extends State<MainNavigation> {

  int currentIndex = 1;

  final screens = const [

    ReportsScreen(),

    HomeScreen(),

    ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      body: screens[currentIndex],

      bottomNavigationBar:
          NavigationBar(

        selectedIndex:
            currentIndex,

        onDestinationSelected:
            (value) {

          setState(() {
            currentIndex = value;
          });
        },

        destinations: const [

          NavigationDestination(
            icon: Icon(
              Icons.warning,
            ),
            label:
                'Reports',
          ),

          NavigationDestination(
            icon: Icon(
              Icons.map,
            ),
            label:
                'Map',
          ),

          NavigationDestination(
            icon: Icon(
              Icons.person,
            ),
            label:
                'Profile',
          ),
        ],
      ),
    );
  }
}