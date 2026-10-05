import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../providers/reports_provider.dart';

class ReportsScreen extends StatefulWidget {
  const ReportsScreen({
    super.key,
  });

  @override
  State<ReportsScreen> createState() =>
      _ReportsScreenState();
}

class _ReportsScreenState
    extends State<ReportsScreen> {
  
  @override
  void initState() {
    super.initState();

    WidgetsBinding.instance
        .addPostFrameCallback(
      (_) {
        context
            .read<ReportsProvider>()
            .loadReports();
      },
    );
  }

  Widget _filterChip(
      ReportsProvider provider,
      String value,
  ) {
    return Padding(
        padding:
            const EdgeInsets.only(
          right: 8,
        ),
        child: ChoiceChip(
          label: Text(
            value,
          ),
          selected:
              provider.selectedFilter ==
                  value,
          onSelected: (_) {
            provider.applyFilter(
              value,
            );
          },
        ),
    );
  }

  Color _statusColor(
    String status,
  ) {
    switch (status.toUpperCase()) {
      case 'VERIFIED':
        return Colors.green;

      case 'RESOLVED':
        return Colors.blueGrey;

      default:
        return Colors.orange;
    }
  }

  IconData _statusIcon(
    String status,
  ) {
    switch (status.toUpperCase()) {
      case 'VERIFIED':
        return Icons.verified;

      case 'RESOLVED':
        return Icons.check_circle;

      default:
        return Icons.warning;
    }
  }

  String _formatDate(
    DateTime date,
  ) {
    return
        "${date.day}/${date.month}/${date.year}";
  }

  @override
  Widget build(
    BuildContext context,
  ) {
    final provider =
        context.watch<ReportsProvider>();

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'My Reports',
        ),
      ),
      body: provider.loading
        ? const Center(
            child: CircularProgressIndicator(),
          )
        : provider.allReports.isEmpty
            ? const Center(
                child: Column(
                  mainAxisAlignment:
                      MainAxisAlignment.center,
                  children: [
                    Icon(
                      Icons.report_outlined,
                      size: 64,
                      color: Colors.grey,
                    ),
                    SizedBox(height: 12),
                    Text(
                      'No reports submitted yet',
                    ),
                  ],
                ),
              )
            : Column(
                children: [
                  Padding(
                    padding:
                        const EdgeInsets.all(12),
                    child:
                        SingleChildScrollView(
                      scrollDirection:
                          Axis.horizontal,
                      child: Row(
                        children: [
                          _filterChip(
                            provider,
                            'ALL',
                          ),
                          _filterChip(
                            provider,
                            'OPEN',
                          ),
                          _filterChip(
                            provider,
                            'VERIFIED',
                          ),
                          _filterChip(
                            provider,
                            'RESOLVED',
                          ),
                        ],
                      ),
                    ),
                  ),
                  Expanded(
                    child: RefreshIndicator(
                      onRefresh:
                          provider.loadReports,
                      child: provider.reports.isEmpty
                        ? Center(
                            child: Text(
                              'No ${provider.selectedFilter} reports',
                            ),
                          )
                        : ListView.builder(
                        padding:
                            const EdgeInsets.all(
                          12,
                        ),
                        itemCount:
                            provider.reports.length,
                        itemBuilder:
                            (
                          context,
                          index,
                        ) {
                          final report =
                              provider.reports[
                                  index];

                          final statusColor =
                              _statusColor(
                            report.status,
                          );

                          return Card(
                            margin:
                                const EdgeInsets.only(
                              bottom: 12,
                            ),
                            elevation: 2,
                            child: Padding(
                              padding:
                                  const EdgeInsets.all(
                                16,
                              ),
                              child: Column(
                                crossAxisAlignment:
                                    CrossAxisAlignment
                                        .start,
                                children: [
                                  Row(
                                    children: [
                                      CircleAvatar(
                                        backgroundColor:
                                            statusColor,
                                        child: Icon(
                                          _statusIcon(
                                            report.status,
                                          ),
                                          color: Colors
                                              .white,
                                        ),
                                      ),
                                      const SizedBox(
                                        width: 12,
                                      ),
                                      Expanded(
                                        child: Text(
                                          report
                                              .category,
                                          style:
                                              const TextStyle(
                                            fontSize:
                                                18,
                                            fontWeight:
                                                FontWeight
                                                    .bold,
                                          ),
                                        ),
                                      ),
                                      Container(
                                        padding:
                                            const EdgeInsets.symmetric(
                                          horizontal:
                                              10,
                                          vertical:
                                              6,
                                        ),
                                        decoration:
                                            BoxDecoration(
                                          color:
                                              statusColor
                                                  .withValues(
                                            alpha:
                                                0.15,
                                          ),
                                          borderRadius:
                                              BorderRadius.circular(
                                            20,
                                          ),
                                        ),
                                        child: Text(
                                          report
                                              .status,
                                          style:
                                              TextStyle(
                                            color:
                                                statusColor,
                                            fontWeight:
                                                FontWeight
                                                    .bold,
                                          ),
                                        ),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(
                                    height: 16,
                                  ),
                                  Text(
                                    report
                                        .description,
                                  ),
                                  const SizedBox(
                                    height: 12,
                                  ),
                                  Row(
                                    children: [
                                      const Icon(
                                        Icons.location_on,
                                        size: 16,
                                        color:
                                            Colors.grey,
                                      ),
                                      const SizedBox(
                                        width: 4,
                                      ),
                                      Text(
                                        report
                                            .regionName,
                                        style:
                                            const TextStyle(
                                          color:
                                              Colors.grey,
                                        ),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(
                                    height: 8,
                                  ),
                                  Row(
                                    children: [
                                      const Icon(
                                        Icons.speed,
                                        size: 16,
                                        color:
                                            Colors.grey,
                                      ),
                                      const SizedBox(
                                        width: 4,
                                      ),
                                      Text(
                                        'Severity ${report.severity}',
                                        style:
                                            const TextStyle(
                                          color:
                                              Colors.grey,
                                        ),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(
                                    height: 8,
                                  ),
                                  Row(
                                    children: [
                                      const Icon(
                                        Icons.calendar_today,
                                        size: 16,
                                        color:
                                            Colors.grey,
                                      ),
                                      const SizedBox(
                                        width: 4,
                                      ),
                                      Text(
                                        _formatDate(
                                          report
                                              .timestamp,
                                        ),
                                        style:
                                            const TextStyle(
                                          color:
                                              Colors.grey,
                                        ),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(
                                    height: 16,
                                  ),
                                  if (report.status !=
                                      'RESOLVED')
                                    SizedBox(
                                      width: double
                                          .infinity,
                                      child:
                                          FilledButton.icon(
                                        icon:
                                            const Icon(
                                          Icons
                                              .check,
                                        ),
                                        label:
                                            const Text(
                                          'Mark Resolved',
                                        ),
                                        onPressed:
                                            () async {
                                          final messenger =
                                              ScaffoldMessenger.of(
                                            context,
                                          );

                                          await provider
                                              .closeReport(
                                            report.id,
                                          );

                                          if (!mounted) {
                                            return;
                                          }

                                          messenger
                                              .showSnackBar(
                                            const SnackBar(
                                              content:
                                                  Text(
                                                'Report resolved',
                                              ),
                                            ),
                                          );
                                        },
                                      ),
                                    )
                                  else
                                    const Row(
                                      mainAxisAlignment:
                                          MainAxisAlignment
                                              .center,
                                      children: [
                                        Icon(
                                          Icons
                                              .check_circle,
                                          color:
                                              Colors.green,
                                        ),
                                        SizedBox(
                                          width: 8,
                                        ),
                                        Text(
                                          'Resolved',
                                        ),
                                      ],
                                    ),
                                ],
                              ),
                            ),
                          );
                        },
                      ),
                    ),
                  ),
                ],
              ),
    );
  }
}