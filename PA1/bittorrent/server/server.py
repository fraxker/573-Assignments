import libtorrent as lt
from pathlib import Path

DATAFILES = Path("../Datafiles")

ATenKB = DATAFILES.joinpath("A_10kB")
AHundredKB = DATAFILES.joinpath("A_100kB")
AOneMB = DATAFILES.joinpath("A_1MB")
ATenMB = DATAFILES.joinpath("A_10MB")

if __name__ == "__main__":
    ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})
    h = ses.add_torrent({'ti': lt.torrent_info('../A_10kB.torrent'), 'save_path': "." , "flags": lt.add_torrent_params_flags_t.default_flags ^ lt.add_torrent_params_flags_t.flag_seed_mode})
    print(h.trackers())
    h.add_tracker("http://localhost:6969/announce")
    # h = ses.add_torrent({'ti': lt.torrent_info('../A_100kB.torrent'), 'save_path': ".", "flags": lt.add_torrent_params_flags_t.default_flags ^ lt.add_torrent_params_flags_t.flag_seed_mode})
    # h = ses.add_torrent({'ti': lt.torrent_info('../A_1MB.torrent'), 'save_path': "." , "flags": lt.add_torrent_params_flags_t.default_flags ^ lt.add_torrent_params_flags_t.flag_seed_mode})
    # h = ses.add_torrent({'ti': lt.torrent_info('../A_10MB.torrent'), 'save_path': "." , "flags": lt.add_torrent_params_flags_t.default_flags ^ lt.add_torrent_params_flags_t.flag_seed_mode})
    s = h.status()
    while True:
        s = h.status()
        print('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % (
        s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
        s.num_peers, s.state), end=' ')

        alerts = ses.pop_alerts()
        for a in alerts:
            if a.category() & lt.alert.category_t.error_notification:
                print(a)
                ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})
                h = ses.add_torrent({'ti': lt.torrent_info('../A_10kB.torrent'), 'save_path': "." , "flags": lt.add_torrent_params_flags_t.default_flags ^ lt.add_torrent_params_flags_t.flag_seed_mode})
                # h = ses.add_torrent({'ti': lt.torrent_info('../A_100kB.torrent'), 'save_path': "." , "flags": lt.add_torrent_params_flags_t.default_flags ^ lt.add_torrent_params_flags_t.flag_seed_mode})
                # h = ses.add_torrent({'ti': lt.torrent_info('../A_1MB.torrent'), 'save_path': "." , "flags": lt.add_torrent_params_flags_t.default_flags ^ lt.add_torrent_params_flags_t.flag_seed_mode})
                # h = ses.add_torrent({'ti': lt.torrent_info('../A_10MB.torrent'), 'save_path': ".", "flags": lt.add_torrent_params_flags_t.default_flags ^ lt.add_torrent_params_flags_t.flag_seed_mode})