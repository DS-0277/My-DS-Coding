import { useParams, useNavigate } from "react-router";
import { posts } from "../data/posts";

export default function PostView() {

    const params = useParams();
    const navigate = useNavigate();

    const post = posts.find((p) => p.id === Number(params.postId));

    if (!post) {
        return <p>Post Not Found</p>
    }

    return (
        <div>
            <h1>{post.title}</h1>
            <p>{post.content}</p>
            <button onClick={() => navigate("/")}>Return to Feed</button>
        </div>
    );
}