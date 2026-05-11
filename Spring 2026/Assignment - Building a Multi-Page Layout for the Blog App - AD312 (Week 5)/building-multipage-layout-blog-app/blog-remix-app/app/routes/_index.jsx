import { posts } from "../data/posts"
import { Link } from "react-router";


export default function Home() {
    return (
        <div>
            <h1>Blog Feed</h1>
            {posts.map((post) => (
                <div key={post.id}>
                    <Link to={`/post/${post.id}`}>{post.title}</Link>
                </div>
            ))}
        </div>
    );
}

// TEST CASES:

// Normal Cases:
// Case 1: Click "About" ==> Go to "About" page as expected
// Case 2: Click "React Router Tips" ==> Go to "React Router Tips" page as expected
// Case 3: Click "Return to Feed" button ==> Go back to homepage

// Edge Cases:
// Case 1: Click "Home" while being in "The Future of Web" page ==> Go back to homepage
// Case 2: Go to path "/post/4" ==> Show "Post Not Found" message
// Case 3: Go to path "/post/a" ==> Show "Post Not Found" message