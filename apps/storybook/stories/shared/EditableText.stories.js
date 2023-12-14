import { EditableText } from "@uoisfrontend/shared";
import { CheckLg, TrashFill } from "react-bootstrap-icons";
import { action } from '@storybook/addon-actions';
import { withRouter } from 'storybook-addon-react-router-v6';

const meta = {
    //👇 component which is all about
    component: EditableText,
    //👇 Tree position where those stories will be placed
    title: "Shared/EditableText",
    //👇 Needed for componets using react-router library
    decorators: [withRouter],

    //👇 Args for the component's play
    argTypes: {
        onChange: {action: "changed"},
    },
    //👇 Enables auto-generated documentation for the component story
    tags: ['autodocs'],
};

export default meta;

/*
 *👇 Render functions are a framework specific feature to allow you control on how the component renders.
 * See https://storybook.js.org/docs/react/api/csf
 * to learn how to use render functions.
 */
export const EditableTextStory = {
    name: "Editeable Text",
    //👇 Initial value for args
    args: {
        value: "Some name",
        // onChange: (value) => action("got " + value)
    },
    parameters: {
        reactRouter: {
            routePath: '/users/:userId',
            routeParams: { userId: '42' },
            routeHandle: "Profile",
            searchParams: { tab: 'activityLog' },
            routeState: { fromPage: 'homePage' },
        }
      },
    
    //👇 how the component will be rendered
    render: (args) => <EditableText id="97e076a0-bbc9-40a4-9a71-1ef85f43b704" value={args.value} onChange={args.onChange} />,
};