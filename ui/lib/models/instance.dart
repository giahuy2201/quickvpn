class Instance {
  final String label;
  String country;
  String region;
  String status;
  String ipv4;
  String ipv6;
  String expiration;

  Instance(
      {required this.label,
      required this.country,
      required this.region,
      required this.status,
      required this.ipv4,
      required this.ipv6,
      required this.expiration});

  factory Instance.fromJson(Map<String, dynamic> json) {
    return switch (json) {
      {
        'label': String label,
        'country': String country,
        'region': String region,
        'status': String status,
        'ipv4': String ipv4,
        'ipv6': String ipv6,
        'expiration': String expiration,
      } =>
        Instance(
          label: label,
          country: country,
          region: region,
          status: status,
          ipv4: ipv4,
          ipv6: ipv6,
          expiration: expiration,
        ),
      _ => throw const FormatException('Failed to load instance.'),
    };
  }
}
