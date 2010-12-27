import scriptcontext
import utility as rhutil

def AddGroup( group_name=None ):
    """
    Adds a new empty group to the document
    Parameters:
      group_name[opt] = name of the new group. If omitted, rhino automatically
          generates the group name
    Returns:
      name of the new group if successful
      None is not successful or on error
    """
    index = -1
    if group_name is None: index = scriptcontext.doc.Groups.Add()
    else: index = scriptcontext.doc.Groups.Add( str(group_name) )
    rc = scriptcontext.doc.Groups.GroupName(index)
    if rc is None: return scriptcontext.errorhandler()
    return rc


def AddObjectsToGroup( object_ids, group_name ):
    """
    Adds one or more objects to an existing group. Neither the objects nor the group can be reference objects
    Parameters:
      object_ids = list of Strings or Guids representing the object identifiers
      group_name = the name of an existing group
    Returns:
      number of objects added to the group
    """
    index = scriptcontext.doc.Groups.Find(str(group_name), True)
    if( index<0 or object_ids==None ): return 0
    if( type(object_ids) is not list ): object_ids = [object_ids]
    ids = []
    for id in object_ids:
        id = rhutil.coerceguid(id)
        if id is not None: ids.append(id)
    if not ids: return 0
    if not scriptcontext.doc.Groups.AddToGroup(index, ids): return 0
    return len(ids)


def AddObjectToGroup( object_id, group_name ):
    """
    Adds a single object to an existing group. Neither the object nor the
    group can be reference objects
    Parameters:
      object_id = String or Guid representing the object identifier
      group_name = the name of an existing group
    Returns:
      True or False representing success or failure
    """
    object_id = rhutil.coerceguid(object_id)
    index = scriptcontext.doc.Groups.Find(str(group_name), True)
    if object_id is None or index<0: return False
    return scriptcontext.doc.Groups.AddToGroup(index, object_id)


def DeleteGroup( group_name ):
    """
    Removes an existing group from the document. Reference groups cannot be
    removed. Deleting a group does not delete the member objects
    Parameters:
      group_name = the name of an existing group
    Returns:
      True or False representing success or failure
    """
    index = scriptcontext.doc.Groups.Find(str(group_name), True)
    return scriptcontext.doc.Groups.Delete(index)


def GroupCount():
    "Returns the number of groups in the document"
    return scriptcontext.doc.Groups.Count


def GroupNames():
    """
    Returns the names of all the groups in the document
    None if no names exist in the document
    """
    names = scriptcontext.doc.Groups.GroupNames(True)
    if names is None: return None
    return list(names)


def HideGroup( group_name ):
    """
    Hides a group of objects. Hidden objects are not visible, cannot be
    snapped to, and cannot be selected
    Parameters:
      group_name = the name of an existing group
    Returns:
      The number of objects that were hidden
    """
    index = scriptcontext.doc.Groups.Find(group_name, True)
    if index<0: return 0
    return scriptcontext.doc.Groups.Hide(index);


def IsGroup( group_name ):
    """
    Verifies the existance of a group
    Paramters:
      group_name = the name of the group to check for
    Returns:
      True or False
    """
    return scriptcontext.doc.Groups.Find(str(group_name), True)>=0


def IsGroupEmpty( group_name ):
    """
    Verifies that an existing group is empty, or contains no object members
    Parameters:
      group_name = the name of an existing group
    Returns:
      True or False if group_name exists
      None if group_name does not exist
    """
    index = scriptcontext.doc.Groups.Find(str(group_name), True)
    if index<0: return scriptcontext.errorhandler()
    return scriptcontext.doc.Groups.GroupObjectCount(index)>0


def LockGroup( group_name ):
    """
    Locks a group of objects. Locked objects are visible and they can be
    snapped to. But, they cannot be selected
    Parameters:
      group_name = the name of an existing group
    Returns:
      Number of objects that were locked if successful
      None on error
    """
    index = scriptcontext.doc.Groups.Find(str(group_name), True)
    if index<0: return scriptcontext.errorhandler()
    return scriptcontext.doc.Groups.Lock(index);


def RemoveObjectFromAllGroups( object_id ):
    """
    Removes a single object from any and all groups that it is a member.
    Neither the object nor the group can be reference objects
    Parameters:
      object_id = the object identifier
    Returns:
      True or False indicating success or failure
    """
    object_id = rhutil.coerceguid(object_id)
    if object_id is None: return False
    rhinoobject = scriptcontext.doc.Objects.Find(object_id)
    if rhinoobject is None or rhinoobject.GroupCount<1: return False
    attrs = rhinoobject.Attributes
    attrs.RemoveFromAllGroups()
    return scriptcontext.doc.Objects.ModifyAttributes(rhinoobject, attrs, True)


def RemoveObjectFromGroup( object_id, group_name ):
    """
    Remove a single object from an existing group
    Parameters:
      object_id = the object identifier
      group_name = the name of an existing group
    Returns:
      True or False indicating success or failure
    """
    count = RemoveObjectsFromGroup(object_id, group_name)
    return not (count is None or count<1)


def RemoveObjectsFromGroup( object_ids, group_name ):
    """
    Removes one or more objects from an existing group
    Parameters:
      object_ids = a list of object identifiers
      group_name = the name of an existing group
    Returns:
      The number of objects removed from the group is successful
      None on error
    """
    index = scriptcontext.doc.Groups.Find(str(group_name), True)
    if object_ids is None or index<0: return scriptcontext.errorhandler()
    if rhutil.coerceguid(objects_ids) is not None:
        object_ids = [object_ids]
    objects_removed = 0
    for id in object_ids:
        id = rhutil.coerceguid(id)
        if id is None: continue
        rhinoobject = scriptcontext.doc.Objects.Find(id)
        if rhinoobect is None: continue
        attrs = rhinoobject.Attributes
        attrs.RemoveFromGroup(index)
        if scriptcontext.doc.Objects.ModifyAttributes(rhinoobject, attrs, True):
            objects_removed += 1
    return objects_removed


def RenameGroup( old_name, new_name ):
    """
    Renames an existing group
    Parameters:
      old_name = the name of an existing group
      new_name = the new group name
    Returns:
      the new group name if successful
      None on error
    """
    index = scriptcontext.doc.Groups.Find(str(old_name), True)
    if index<0: return scriptcontext.errorhandler()
    if scriptcontext.doc.Groups.ChangeGroupName(index, str(new_name)):
        return new_name
    return scriptcontext.errorhandler()


def ShowGroup( group_name ):
    """
    Shows a group of previously hidden objects. Hidden objects are not visible,
    cannot be snapped to, and cannot be selected
    Parameters:
      group_name = the name of an existing group
    Returns:
      The number of objects that were shown if successful
      None on error  
    """
    index = scriptcontext.doc.Groups.Find(str(group_name), True)
    if index<0: return scriptcontext.errorhandler()
    return scriptcontext.doc.Groups.Show(index);


def UnlockGroup( group_name ):
    """
    Unlocks a group of previously locked objects. Lockes objects are visible,
    can be snapped to, but cannot be selected
    Parameters:
      group_name = the name of an existing group
    Returns:
      The number of objects that were unlocked if successful
      None on error  
    """
    index = scriptcontext.doc.Groups.Find(str(group_name), True)
    if index<0: return scriptcontext.errorhandler()
    return scriptcontext.doc.Groups.Unlock(index);