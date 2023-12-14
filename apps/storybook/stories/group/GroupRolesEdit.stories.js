import { withRouter } from 'storybook-addon-react-router-v6';

import { StorageDecorator } from "../StorageDecorator";
import { GroupDecorator } from "./GroupDecorator";
import { GroupRolesEdit } from '@uoisfrontend/group';

const meta = {
    //👇 component which is all about
    component: GroupRolesEdit,
    //👇 Tree position where those stories will be placed
    title: "Group/GroupRolesEdit",
    
    //👇 Needed for componets using react-router library
    //   also for components using useDispatch hook
    decorators: [GroupDecorator, StorageDecorator, withRouter], //order has a mean

    //👇 Args for the component's play
    // argTypes: {
    //     onChange: {action: "changed"},
    // },
    //👇 Enables auto-generated documentation for the component story
    tags: ['autodocs'],

};

export default meta;

/*
 *👇 Render functions are a framework specific feature to allow you control on how the component renders.
 * See https://storybook.js.org/docs/react/api/csf
 * to learn how to use render functions.
 */
export const GroupRolesEditStory = {
    name: "group roles edit",
    //👇 Initial value for args
    args: {
        // onChange: (value) => action("got " + value)
        group: {
            id: "2d9dcd22-a4a2-11ed-b9df-0242ac120003"
        },
        onlyValid: true,
        onlyInvalid: false
    },
    parameters: {
        reactRouter: {
            routePath: '/ui/groups/:groupId',
            routeParams: { groupId: '2d9dcd22-a4a2-11ed-b9df-0242ac120003' },
            routeHandle: "Profile",
            searchParams: { tab: 'activityLog' },
            routeState: { fromPage: 'homePage' },
        },
        // docs: { iframeHeight: 600 } 
      },
    
    //👇 how the component will be rendered
    render: (args) => <GroupRolesEdit group={args.group} onlyValid={args.onlyValid} onlyInvalid={args.onlyInvalid}/>,
};