import requests


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")

    def get(self, endpoint, params=None):
        response = requests.get(
            f"{self.base_url}/{endpoint.lstrip('/')}",
            params=params
        )
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None):
        response = requests.post(
            f"{self.base_url}/{endpoint.lstrip('/')}",
            json=data
        )
        response.raise_for_status()
        return response.json()


class JSONPlaceholderClient(APIClient):
    def __init__(self):
        super().__init__("https://jsonplaceholder.typicode.com")

    def get_user(self, user_id):
        """Get a specific user's profile."""
        return self.get(f"users/{user_id}")

    def get_user_posts(self, user_id):
        """Get all posts by a specific user."""
        return self.get("posts", params={"userId": user_id})

    def create_post(self, user_id, title, body):
        """Create a new post for a user."""
        post_data = {
            "userId": user_id,
            "title": title,
            "body": body
        }
        return self.post("posts", data=post_data)

    def search_posts(self, query):
        """Search posts by title (client-side filtering)."""
        posts = self.get("posts")

        return [
            post for post in posts
            if query.lower() in post["title"].lower()
        ]


def main():
    client = JSONPlaceholderClient()

    # Get user 5's profile
    user = client.get_user(5)
    print("User 5:")
    print(f"Name: {user['name']}")
    print(f"City: {user['address']['city']}")
    print()

    # Get user 5's posts
    posts = client.get_user_posts(5)
    print(f"User 5 post count: {len(posts)}")
    print()

    # Create a new post
    new_post = client.create_post(
        user_id=5,
        title="Learning APIs",
        body="This post was created using my API client."
    )

    print(f"New post ID: {new_post['id']}")
    print()

    # Search posts
    matches = client.search_posts("qui")
    print(f"Posts with 'qui' in title: {len(matches)}")


if __name__ == "__main__":
    main()