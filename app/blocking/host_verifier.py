from .requester import requester
from .visited import visited
from .metadata import metadata


class HostVerifier:

    @staticmethod
    def is_valid(pr):
        if not (pr.scheme or pr.netloc):
            return True

        with visited:
            if pr.netloc in visited.accepted_hosts:
                return True
            if pr.netloc in visited.rejected_hosts:
                return False

        if not pr.netloc.endswith(metadata.domain):
            visited.rejected_hosts.add(pr.netloc)
            return False

        base_url = f"{pr.scheme}://{pr.netloc}"
        res = requester.head(base_url)

        with visited:
            if res.ok:
                visited.accepted_hosts.add(pr.netloc)
                return True
            else:
                visited.rejected_hosts.add(pr.netloc)
                return False
