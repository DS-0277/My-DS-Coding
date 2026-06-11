export default function BuggyComponent() {
    throw new Error('Server Error');
    return <h2>Hello</h2>
}