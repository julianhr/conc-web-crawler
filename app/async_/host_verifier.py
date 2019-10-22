from .requester import requester
from .visited import visited
from .metadata import metadata


class HostVerifier:

    @staticmethod
    async def is_valid(pr):
        if not (pr.scheme or pr.netloc):
            return True

        if pr.netloc in visited.accepted_hosts:
            return True
        if pr.netloc in visited.rejected_hosts:
            return False

        if not pr.netloc.endswith(metadata.domain):
            visited.rejected_hosts.add(pr.netloc)
            return False

        base_url = f"{pr.scheme}://{pr.netloc}"
        res = await requester.head(base_url)

        if res.status < 400:
            visited.accepted_hosts.add(pr.netloc)
            return True
        else:
            visited.rejected_hosts.add(pr.netloc)
            return False
