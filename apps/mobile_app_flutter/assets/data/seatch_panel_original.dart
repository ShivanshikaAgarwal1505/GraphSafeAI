// import 'package:flutter/material.dart';
// import 'package:provider/provider.dart';

// import '../../navigation/providers/navigation_provider.dart';
// import '../models/search_location.dart';
// import '../providers/search_provider.dart';

// class SearchPanel extends StatefulWidget {
//   const SearchPanel({super.key});

//   static final GlobalKey<_SearchPanelState>
//     panelKey =
//         GlobalKey<_SearchPanelState>();

//   @override
//   State<SearchPanel> createState() =>
//       _SearchPanelState();
// }

// class _SearchPanelState
//     extends State<SearchPanel> {
//   final sourceController =
//       TextEditingController();

//   final destinationController =
//       TextEditingController();

//   bool expanded = false;

//   bool editingSource = false;

//   bool showSuggestions = false;

//   @override
//   void dispose() {
//     sourceController.dispose();
//     destinationController.dispose();
//     super.dispose();
//   }

//   void collapseSuggestions() {
//     if (!mounted) return;

//     setState(() {
//       showSuggestions = false;
//       editingSource = false;
//     });
//   }

//   Future<void> _refreshRoute(
//     BuildContext context,
//     SearchProvider provider,
//   ) async {
//     final nav =
//         context.read<NavigationProvider>();

//     final source =
//         provider.selectedSource;

//     final destination =
//         provider.selectedDestination;

//     if (destination == null) {
//       return;
//     }

//     final sourceLat =
//         source?.isCurrentLocation == true
//             ? nav.sourceLat
//             : source?.latitude ??
//                 nav.sourceLat;

//     final sourceLon =
//         source?.isCurrentLocation == true
//             ? nav.sourceLon
//             : source?.longitude ??
//                 nav.sourceLon;

//     final destinationLat = destination.isCurrentLocation ? nav.sourceLat: destination.latitude;

//     final destinationLon = destination.isCurrentLocation? nav.sourceLon : destination.longitude;
//     await nav.loadRoute(
//       sourceLat: sourceLat,
//       sourceLon: sourceLon,
//       destinationLat:
//           destinationLat,
//       destinationLon:
//           destinationLon,
//     );
//   }

//   @override
//   Widget build(BuildContext context) {
//     final provider =
//         context.watch<SearchProvider>();

//     return Material(
//       elevation: 8,
//       color: Colors.white,
//       borderRadius:
//           BorderRadius.circular(20),
//       child: Column(
//         mainAxisSize:
//             MainAxisSize.min,
//         children: [
//           if (!expanded &&
//               provider.selectedDestination ==
//                   null)
//             InkWell(
//               borderRadius:
//                   BorderRadius.circular(
//                 20,
//               ),
//               onTap: () {
//                 setState(() {
//                   expanded = true;
//                   showSuggestions =
//                       true;
//                 });
//               },
//               child: const Padding(
//                 padding:
//                     EdgeInsets.all(16),
//                 child: Row(
//                   children: [
//                     Icon(Icons.search),
//                     SizedBox(width: 12),
//                     Expanded(
//                       child: Text(
//                         'Where are you going?',
//                       ),
//                     ),
//                   ],
//                 ),
//               ),
//             ),

//           if (expanded ||
//               provider.selectedDestination !=
//                   null)
//             Stack(
//               children: [
//                 Column(
//                   children: [
//                     InkWell(
//                       onTap: () {
//                         setState(() {
//                           editingSource =
//                               true;
//                           showSuggestions =
//                               true;
//                           sourceController
//                               .clear();
//                         });
//                       },
//                       child: Padding(
//                         padding:
//                             const EdgeInsets.symmetric(
//                           horizontal: 16,
//                           vertical: 14,
//                         ),
//                         child: Row(
//                           children: [
//                             const Icon(
//                               Icons.my_location,
//                               color:
//                                   Colors.green,
//                             ),
//                             const SizedBox(
//                               width: 12,
//                             ),
//                             Expanded(
//                               child: editingSource
//                                   ? TextField(
//                                       controller:
//                                           sourceController,
//                                       autofocus:
//                                           true,
//                                       onChanged:
//                                           provider
//                                               .search,
//                                       decoration:
//                                           const InputDecoration(
//                                         border:
//                                             InputBorder.none,
//                                         hintText:
//                                             'Search source',
//                                         isDense:
//                                             true,
//                                       ),
//                                     )
//                                   : Text(
//                                       provider.selectedSource
//                                               ?.name ??
//                                           'Current Location',
//                                       style: Theme.of(
//                                               context)
//                                           .textTheme
//                                           .bodyLarge,
//                                     ),
//                             ),
//                           ],
//                         ),
//                       ),
//                     ),

//                     const Divider(
//                       height: 1,
//                     ),

//                     Padding(
//                       padding:
//                           const EdgeInsets.symmetric(
//                         horizontal: 16,
//                         vertical: 8,
//                       ),
//                       child: Row(
//                         children: [
//                           const Icon(
//                             Icons.search,
//                           ),
//                           const SizedBox(
//                             width: 12,
//                           ),
//                           Expanded(
//                             child: TextField(
//                               controller:
//                                   destinationController,
//                               onTap: () {
//                                 setState(() {
//                                   editingSource =
//                                       false;
//                                   showSuggestions =
//                                       true;
//                                 });
//                               },
//                               onChanged:
//                                   provider.search,
//                               decoration:
//                                   InputDecoration(
//                                 border:
//                                     InputBorder.none,
//                                 isDense:
//                                     true,
//                                 hintText: provider
//                                         .selectedDestination
//                                         ?.name ??
//                                     'Search destination',
//                               ),
//                             ),
//                           ),
//                         ],
//                       ),
//                     ),

//                     if (showSuggestions)
//                       const Divider(
//                         height: 1,
//                       ),

//                     if (showSuggestions)
//                       SizedBox(
//                         height: 280,
//                         child: ListView(
//                           children: [
//                             _currentLocationTile(
//                               context,
//                               provider,
//                             ),

//                             const _SectionHeader(
//                               title:
//                                   'Favorites',
//                             ),

//                             if (provider
//                                 .favoritePlaces
//                                 .isEmpty)
//                               const ListTile(
//                                 title: Text(
//                                   'No favorites yet',
//                                 ),
//                               ),

//                             ...provider
//                                 .favoritePlaces
//                                 .map(
//                               (e) => _item(
//                                 context,
//                                 provider,
//                                 e,
//                                 Icons.star,
//                               ),
//                             ),

//                             if (provider
//                                 .recentSearches
//                                 .isNotEmpty) ...[
//                               const _SectionHeader(
//                                 title:
//                                     'Recent Searches',
//                               ),
//                               ...provider
//                                   .recentSearches
//                                   .map(
//                                 (e) => _item(
//                                   context,
//                                   provider,
//                                   e,
//                                   Icons.history,
//                                 ),
//                               ),
//                             ],

//                             const _SectionHeader(
//                               title:
//                                   'Popular Places',
//                             ),

//                             ...provider
//                                 .popularPlaces
//                                 .map(
//                               (e) => _item(
//                                 context,
//                                 provider,
//                                 e,
//                                 Icons.place,
//                               ),
//                             ),

//                             if (provider
//                                 .filteredResults
//                                 .isNotEmpty) ...[
//                               const _SectionHeader(
//                                 title:
//                                     'Results',
//                               ),
//                               ...provider
//                                   .filteredResults
//                                   .map(
//                                 (e) => _item(
//                                   context,
//                                   provider,
//                                   e,
//                                   Icons.place,
//                                 ),
//                               ),
//                             ],
//                           ],
//                         ),
//                       ),
//                   ],
//                 ),

//                 if (provider
//                         .selectedDestination !=
//                     null || provider.selectedSource != null)
//                   Positioned(
//                     right: 8,
//                     top: 38,
//                     child: Material(
//                       elevation: 3,
//                       shape:
//                           const CircleBorder(),
//                       child: IconButton(
//                         icon: const Icon(
//                           Icons.swap_vert,
//                         ),
//                         onPressed:
//                             () async {
//                           provider
//                               .swapLocations();

//                           sourceController
//                                   .text =
//                               provider
//                                       .selectedSource
//                                       ?.name ??
//                                   '';

//                           destinationController
//                                   .text =
//                               provider
//                                       .selectedDestination
//                                       ?.name ??
//                                   '';

//                           await _refreshRoute(
//                             context,
//                             provider,
//                           );

//                           if (!mounted) {
//                             return;
//                           }

//                           setState(() {});
//                         },
//                       ),
//                     ),
//                   ),
//               ],
//             ),
//         ],
//       ),
//     );
//   }

//   Widget _currentLocationTile(
//     BuildContext context,
//     SearchProvider provider,
//   ) {
//     return ListTile(
//       leading: const Icon(
//         Icons.my_location,
//         color: Colors.green,
//       ),
//       title: const Text(
//         'Use Current Location',
//       ),
//       onTap: () async {
//         provider.setSource(
//           SearchLocation.current(),
//         );

//         await _refreshRoute(
//           context,
//           provider,
//         );

//         setState(() {
//           editingSource = false;
//           showSuggestions =
//               false;
//         });
//       },
//     );
//   }

//   Widget _item(
//     BuildContext context,
//     SearchProvider provider,
//     SearchLocation location,
//     IconData icon,
//   ) {
//     return ListTile(
//       leading: Icon(icon),
//       title: Text(location.name),
//       onTap: () async {
//         if (editingSource) {
//           provider.setSource(
//             location,
//           );

//           await _refreshRoute(
//             context,
//             provider,
//           );

//           setState(() {
//             editingSource = false;
//             showSuggestions =
//                 false;
//           });

//           return;
//         }

//         await provider
//             .setDestination(
//           location,
//         );

//         destinationController.text =
//             location.name;

//         await _refreshRoute(
//           context,
//           provider,
//         );

//         setState(() {
//           showSuggestions = false;
//           expanded = true;
//         });
//       },
//     );
//   }
// }

// class _SectionHeader
//     extends StatelessWidget {
//   final String title;

//   const _SectionHeader({
//     required this.title,
//   });

//   @override
//   Widget build(BuildContext context) {
//     return Padding(
//       padding:
//           const EdgeInsets.only(
//         left: 16,
//         top: 12,
//         bottom: 6,
//       ),
//       child: Text(
//         title,
//         style: const TextStyle(
//           fontWeight:
//               FontWeight.bold,
//         ),
//       ),
//     );
//   }
// }